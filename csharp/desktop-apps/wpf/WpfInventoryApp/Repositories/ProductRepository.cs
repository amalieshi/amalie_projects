using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using WpfInventoryApp.Data;
using WpfInventoryApp.Models;

namespace WpfInventoryApp.Repositories;

public class ProductRepository : IProductRepository
{
    private readonly InventoryDbContext _context;
    private readonly ILogger<ProductRepository> _logger;
    private bool _disposed = false;

    public ProductRepository(InventoryDbContext context, ILogger<ProductRepository> logger)
    {
        _context = context ?? throw new ArgumentNullException(nameof(context));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    public async Task<IEnumerable<Product>> GetAllAsync()
    {
        try
        {
            _logger.LogDebug("Retrieving all products");
            return await _context.Products.OrderBy(p => p.Name).ToListAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while retrieving all products");
            throw;
        }
    }

    public async Task<Product?> GetByIdAsync(int id)
    {
        try
        {
            _logger.LogDebug("Retrieving product with ID: {ProductId}", id);
            return await _context.Products.FindAsync(id);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while retrieving product with ID: {ProductId}", id);
            throw;
        }
    }

    public async Task<Product?> GetBySkuAsync(string sku)
    {
        try
        {
            _logger.LogDebug("Retrieving product with SKU: {ProductSku}", sku);
            return await _context.Products.FirstOrDefaultAsync(p => p.SKU == sku);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while retrieving product with SKU: {ProductSku}", sku);
            throw;
        }
    }

    public async Task<Product> AddAsync(Product product)
    {
        try
        {
            if (product == null)
                throw new ArgumentNullException(nameof(product));

            _logger.LogDebug("Adding new product: {ProductName}", product.Name);

            _context.Products.Add(product);
            await _context.SaveChangesAsync();

            _logger.LogInformation("Product added successfully with ID: {ProductId}", product.Id);
            return product;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while adding product: {ProductName}", product?.Name);
            throw;
        }
    }

    public async Task<Product> UpdateAsync(Product product)
    {
        try
        {
            if (product == null)
                throw new ArgumentNullException(nameof(product));

            _logger.LogDebug("Updating product with ID: {ProductId}", product.Id);

            _context.Entry(product).State = EntityState.Modified;
            await _context.SaveChangesAsync();

            _logger.LogInformation("Product updated successfully: {ProductId}", product.Id);
            return product;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while updating product with ID: {ProductId}", product?.Id);
            throw;
        }
    }

    public async Task<bool> DeleteAsync(int id)
    {
        try
        {
            _logger.LogDebug("Deleting product with ID: {ProductId}", id);

            var product = await _context.Products.FindAsync(id);
            if (product == null)
            {
                _logger.LogWarning("Product with ID {ProductId} not found for deletion", id);
                return false;
            }

            _context.Products.Remove(product);
            await _context.SaveChangesAsync();

            _logger.LogInformation("Product deleted successfully: {ProductId}", id);
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while deleting product with ID: {ProductId}", id);
            throw;
        }
    }

    public async Task<bool> ExistsAsync(int id)
    {
        try
        {
            return await _context.Products.AnyAsync(p => p.Id == id);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while checking if product exists with ID: {ProductId}", id);
            throw;
        }
    }

    public async Task<bool> SkuExistsAsync(string sku, int excludeId = 0)
    {
        try
        {
            return await _context.Products.AnyAsync(p => p.SKU == sku && p.Id != excludeId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while checking if SKU exists: {ProductSku}", sku);
            throw;
        }
    }

    public async Task<int> CountAsync()
    {
        try
        {
            return await _context.Products.CountAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while counting products");
            throw;
        }
    }

    protected virtual void Dispose(bool disposing)
    {
        if (!_disposed)
        {
            if (disposing)
            {
                _context?.Dispose();
            }
            _disposed = true;
        }
    }

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }
}