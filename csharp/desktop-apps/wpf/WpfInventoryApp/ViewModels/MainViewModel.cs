using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using Microsoft.Extensions.Logging;
using WpfInventoryApp.Commands;
using WpfInventoryApp.Repositories;

namespace WpfInventoryApp.ViewModels;

public class MainViewModel : ViewModelBase
{
    private readonly IProductRepository _productRepository;
    private readonly ILogger<MainViewModel> _logger;

    private ObservableCollection<ProductViewModel> _products = new();
    private ProductViewModel? _selectedProduct;
    private ProductViewModel _currentProduct = new();
    private bool _isLoading;
    private string _statusMessage = "Ready";
    private bool _isEditMode;

    public ObservableCollection<ProductViewModel> Products
    {
        get => _products;
        set => SetProperty(ref _products, value);
    }

    public ProductViewModel? SelectedProduct
    {
        get => _selectedProduct;
        set
        {
            if (SetProperty(ref _selectedProduct, value))
            {
                OnSelectedProductChanged();
            }
        }
    }

    public ProductViewModel CurrentProduct
    {
        get => _currentProduct;
        set => SetProperty(ref _currentProduct, value);
    }

    public bool IsLoading
    {
        get => _isLoading;
        set => SetProperty(ref _isLoading, value);
    }

    public string StatusMessage
    {
        get => _statusMessage;
        set => SetProperty(ref _statusMessage, value);
    }

    public bool IsEditMode
    {
        get => _isEditMode;
        set => SetProperty(ref _isEditMode, value);
    }

    public string FormTitle => IsEditMode ? "Edit Product" : "Add New Product";

    // Commands
    public ICommand LoadProductsCommand { get; }
    public ICommand AddProductCommand { get; }
    public ICommand UpdateProductCommand { get; }
    public ICommand DeleteProductCommand { get; }
    public ICommand EditProductCommand { get; }
    public ICommand CancelEditCommand { get; }
    public ICommand ClearFormCommand { get; }

    public MainViewModel(IProductRepository productRepository, ILogger<MainViewModel> logger)
    {
        _productRepository = productRepository ?? throw new ArgumentNullException(nameof(productRepository));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));

        // Initialize commands
        LoadProductsCommand = new AsyncRelayCommand(LoadProductsAsync);
        AddProductCommand = new AsyncRelayCommand(AddProductAsync, CanAddProduct);
        UpdateProductCommand = new AsyncRelayCommand(UpdateProductAsync, CanUpdateProduct);
        DeleteProductCommand = new AsyncRelayCommand(DeleteProductAsync, CanDeleteProduct);
        EditProductCommand = new RelayCommand(EditProduct, CanEditProduct);
        CancelEditCommand = new RelayCommand(CancelEdit, () => IsEditMode);
        ClearFormCommand = new RelayCommand(ClearForm);

        // Load initial data
        _ = LoadProductsAsync();
    }

    private async Task LoadProductsAsync()
    {
        try
        {
            IsLoading = true;
            StatusMessage = "Loading products...";
            _logger.LogInformation("Loading products from repository");

            var products = await _productRepository.GetAllAsync();
            var productViewModels = products.Select(p => new ProductViewModel(p)).ToList();

            Products.Clear();
            foreach (var product in productViewModels)
            {
                Products.Add(product);
            }

            StatusMessage = $"Loaded {Products.Count} products";
            _logger.LogInformation("Successfully loaded {ProductCount} products", Products.Count);
        }
        catch (Exception ex)
        {
            StatusMessage = "Error loading products";
            _logger.LogError(ex, "Error occurred while loading products");
            MessageBox.Show($"Error loading products: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }
        finally
        {
            IsLoading = false;
        }
    }

    private async Task AddProductAsync()
    {
        try
        {
            IsLoading = true;
            StatusMessage = "Adding product...";

            // Validate SKU uniqueness
            if (await _productRepository.SkuExistsAsync(CurrentProduct.SKU))
            {
                MessageBox.Show($"A product with SKU '{CurrentProduct.SKU}' already exists.", "Duplicate SKU",
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            var product = CurrentProduct.ToModel();
            var addedProduct = await _productRepository.AddAsync(product);

            var productViewModel = new ProductViewModel(addedProduct);
            Products.Add(productViewModel);
            SelectedProduct = productViewModel;

            ClearForm();
            StatusMessage = "Product added successfully";
            _logger.LogInformation("Product added successfully: {ProductName}", addedProduct.Name);
        }
        catch (Exception ex)
        {
            StatusMessage = "Error adding product";
            _logger.LogError(ex, "Error occurred while adding product");
            MessageBox.Show($"Error adding product: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }
        finally
        {
            IsLoading = false;
        }
    }

    private async Task UpdateProductAsync()
    {
        try
        {
            if (SelectedProduct == null) return;

            IsLoading = true;
            StatusMessage = "Updating product...";

            // Validate SKU uniqueness (excluding current product)
            if (await _productRepository.SkuExistsAsync(CurrentProduct.SKU, CurrentProduct.Id))
            {
                MessageBox.Show($"A product with SKU '{CurrentProduct.SKU}' already exists.", "Duplicate SKU",
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            var product = CurrentProduct.ToModel();
            var updatedProduct = await _productRepository.UpdateAsync(product);

            SelectedProduct.UpdateFromModel(updatedProduct);
            CancelEdit();
            StatusMessage = "Product updated successfully";
            _logger.LogInformation("Product updated successfully: {ProductId}", updatedProduct.Id);
        }
        catch (Exception ex)
        {
            StatusMessage = "Error updating product";
            _logger.LogError(ex, "Error occurred while updating product");
            MessageBox.Show($"Error updating product: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }
        finally
        {
            IsLoading = false;
        }
    }

    private async Task DeleteProductAsync()
    {
        try
        {
            if (SelectedProduct == null) return;

            var result = MessageBox.Show(
                $"Are you sure you want to delete '{SelectedProduct.Name}'?",
                "Confirm Delete",
                MessageBoxButton.YesNo,
                MessageBoxImage.Question);

            if (result != MessageBoxResult.Yes) return;

            IsLoading = true;
            StatusMessage = "Deleting product...";

            var deleted = await _productRepository.DeleteAsync(SelectedProduct.Id);
            if (deleted)
            {
                Products.Remove(SelectedProduct);
                SelectedProduct = null;
                ClearForm();
                StatusMessage = "Product deleted successfully";
                _logger.LogInformation("Product deleted successfully: {ProductId}", SelectedProduct?.Id);
            }
            else
            {
                StatusMessage = "Product not found";
                MessageBox.Show("Product was not found or could not be deleted.", "Delete Failed",
                    MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }
        catch (Exception ex)
        {
            StatusMessage = "Error deleting product";
            _logger.LogError(ex, "Error occurred while deleting product");
            MessageBox.Show($"Error deleting product: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }
        finally
        {
            IsLoading = false;
        }
    }

    private void EditProduct()
    {
        if (SelectedProduct != null)
        {
            CurrentProduct = SelectedProduct.Clone();
            IsEditMode = true;
            StatusMessage = "Editing product";
        }
    }

    private void CancelEdit()
    {
        IsEditMode = false;
        ClearForm();
        StatusMessage = "Edit cancelled";
    }

    private void ClearForm()
    {
        CurrentProduct = new ProductViewModel();
        OnPropertyChanged(nameof(FormTitle));
    }

    private void OnSelectedProductChanged()
    {
        // Refresh command states
        CommandManager.InvalidateRequerySuggested();
    }

    // Command validation methods
    private bool CanAddProduct() => !IsEditMode && !IsLoading && !string.IsNullOrWhiteSpace(CurrentProduct.Name) &&
                                   !string.IsNullOrWhiteSpace(CurrentProduct.SKU) && CurrentProduct.Price > 0;

    private bool CanUpdateProduct() => IsEditMode && !IsLoading && !string.IsNullOrWhiteSpace(CurrentProduct.Name) &&
                                      !string.IsNullOrWhiteSpace(CurrentProduct.SKU) && CurrentProduct.Price > 0;

    private bool CanDeleteProduct() => SelectedProduct != null && !IsLoading && !IsEditMode;

    private bool CanEditProduct() => SelectedProduct != null && !IsLoading && !IsEditMode;

    protected override void Dispose(bool disposing)
    {
        if (disposing)
        {
            _productRepository?.Dispose();
        }
        base.Dispose(disposing);
    }
}