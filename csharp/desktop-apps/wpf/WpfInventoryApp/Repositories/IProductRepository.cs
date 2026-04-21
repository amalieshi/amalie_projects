using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using WpfInventoryApp.Models;

namespace WpfInventoryApp.Repositories;

public interface IProductRepository : IDisposable
{
    Task<IEnumerable<Product>> GetAllAsync();
    Task<Product?> GetByIdAsync(int id);
    Task<Product?> GetBySkuAsync(string sku);
    Task<Product> AddAsync(Product product);
    Task<Product> UpdateAsync(Product product);
    Task<bool> DeleteAsync(int id);
    Task<bool> ExistsAsync(int id);
    Task<bool> SkuExistsAsync(string sku, int excludeId = 0);
    Task<int> CountAsync();
}