using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using WpfInventoryApp.Models;

namespace WpfInventoryApp.ViewModels;

public class ProductViewModel : ViewModelBase
{
    private int _id;
    private string _name = string.Empty;
    private string _sku = string.Empty;
    private int _quantity;
    private decimal _price;
    private DateTime _createdAt;
    private DateTime _updatedAt;
    private bool _isSelected;

    public int Id
    {
        get => _id;
        set => SetProperty(ref _id, value);
    }

    [Required(ErrorMessage = "Product name is required")]
    [StringLength(100, ErrorMessage = "Product name cannot exceed 100 characters")]
    public string Name
    {
        get => _name;
        set => SetProperty(ref _name, value);
    }

    [Required(ErrorMessage = "SKU is required")]
    [StringLength(50, ErrorMessage = "SKU cannot exceed 50 characters")]
    public string SKU
    {
        get => _sku;
        set => SetProperty(ref _sku, value);
    }

    [Range(0, int.MaxValue, ErrorMessage = "Quantity must be non-negative")]
    public int Quantity
    {
        get => _quantity;
        set => SetProperty(ref _quantity, value);
    }

    [Range(0.01, double.MaxValue, ErrorMessage = "Price must be greater than zero")]
    public decimal Price
    {
        get => _price;
        set => SetProperty(ref _price, value);
    }

    public DateTime CreatedAt
    {
        get => _createdAt;
        set => SetProperty(ref _createdAt, value);
    }

    public DateTime UpdatedAt
    {
        get => _updatedAt;
        set => SetProperty(ref _updatedAt, value);
    }

    public bool IsSelected
    {
        get => _isSelected;
        set => SetProperty(ref _isSelected, value);
    }

    public string DisplayText => $"{Name} ({SKU}) - ${Price:F2}";

    public ProductViewModel()
    {
        CreatedAt = DateTime.UtcNow;
        UpdatedAt = DateTime.UtcNow;
    }

    public ProductViewModel(Product product) : this()
    {
        if (product != null)
        {
            Id = product.Id;
            Name = product.Name;
            SKU = product.SKU;
            Quantity = product.Quantity;
            Price = product.Price;
            CreatedAt = product.CreatedAt;
            UpdatedAt = product.UpdatedAt;
        }
    }

    public Product ToModel()
    {
        return new Product
        {
            Id = Id,
            Name = Name,
            SKU = SKU,
            Quantity = Quantity,
            Price = Price,
            CreatedAt = CreatedAt,
            UpdatedAt = UpdatedAt
        };
    }

    public void UpdateFromModel(Product product)
    {
        if (product != null)
        {
            Id = product.Id;
            Name = product.Name;
            SKU = product.SKU;
            Quantity = product.Quantity;
            Price = product.Price;
            CreatedAt = product.CreatedAt;
            UpdatedAt = product.UpdatedAt;
        }
    }

    public ProductViewModel Clone()
    {
        return new ProductViewModel
        {
            Id = Id,
            Name = Name,
            SKU = SKU,
            Quantity = Quantity,
            Price = Price,
            CreatedAt = CreatedAt,
            UpdatedAt = UpdatedAt
        };
    }
}