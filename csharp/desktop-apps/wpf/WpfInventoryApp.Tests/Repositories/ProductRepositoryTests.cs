using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using WpfInventoryApp.Data;
using WpfInventoryApp.Models;
using WpfInventoryApp.Repositories;
using Xunit;

namespace WpfInventoryApp.Tests.Repositories;

public class ProductRepositoryTests : IDisposable
{
    private readonly InventoryDbContext _context;
    private readonly ProductRepository _repository;
    private readonly TestLogger<ProductRepository> _logger;
    private bool _disposed = false;

    public ProductRepositoryTests()
    {
        // Create in-memory database
        var options = new DbContextOptionsBuilder<InventoryDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new InventoryDbContext(options);
        _logger = new TestLogger<ProductRepository>();
        _repository = new ProductRepository(_context, _logger);

        // Ensure database is created
        _context.Database.EnsureCreated();
    }

    // Simple test logger implementation
    private class TestLogger<T> : ILogger<T>
    {
        public IDisposable? BeginScope<TState>(TState state) where TState : notnull => null;
        public bool IsEnabled(LogLevel logLevel) => true;
        public void Log<TState>(LogLevel logLevel, EventId eventId, TState state, Exception? exception, Func<TState, Exception?, string> formatter)
        {
            // Simple implementation for testing - could collect log messages if needed
        }
    }

    [Fact]
    public async Task GetAllAsync_ShouldReturnAllProducts_OrderedByName()
    {
        // Arrange
        var products = new[]
        {
            new Product { Name = "Product C", SKU = "SKU003", Quantity = 30, Price = 30.00m },
            new Product { Name = "Product A", SKU = "SKU001", Quantity = 10, Price = 10.00m },
            new Product { Name = "Product B", SKU = "SKU002", Quantity = 20, Price = 20.00m }
        };

        await _context.Products.AddRangeAsync(products);
        await _context.SaveChangesAsync();

        // Act
        var result = await _repository.GetAllAsync();

        // Assert
        result.Should().HaveCount(4); // 3 + 1 seed data
        result.Should().BeInAscendingOrder(p => p.Name);
    }

    [Fact]
    public async Task GetByIdAsync_WithValidId_ShouldReturnProduct()
    {
        // Arrange
        var product = new Product
        {
            Name = "Test Product",
            SKU = "TEST001",
            Quantity = 5,
            Price = 15.50m
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        // Act
        var result = await _repository.GetByIdAsync(product.Id);

        // Assert
        result.Should().NotBeNull();
        result!.Name.Should().Be("Test Product");
        result.SKU.Should().Be("TEST001");
    }

    [Fact]
    public async Task GetByIdAsync_WithInvalidId_ShouldReturnNull()
    {
        // Act
        var result = await _repository.GetByIdAsync(999);

        // Assert
        result.Should().BeNull();
    }

    [Fact]
    public async Task GetBySkuAsync_WithValidSku_ShouldReturnProduct()
    {
        // Arrange
        var product = new Product
        {
            Name = "SKU Test Product",
            SKU = "SKUTEST001",
            Quantity = 8,
            Price = 25.00m
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        // Act
        var result = await _repository.GetBySkuAsync("SKUTEST001");

        // Assert
        result.Should().NotBeNull();
        result!.Name.Should().Be("SKU Test Product");
    }

    [Fact]
    public async Task GetBySkuAsync_WithInvalidSku_ShouldReturnNull()
    {
        // Act
        var result = await _repository.GetBySkuAsync("NONEXISTENT");

        // Assert
        result.Should().BeNull();
    }

    [Fact]
    public async Task AddAsync_WithValidProduct_ShouldAddSuccessfully()
    {
        // Arrange
        var product = new Product
        {
            Name = "New Product",
            SKU = "NEW001",
            Quantity = 12,
            Price = 45.75m
        };

        // Act
        var result = await _repository.AddAsync(product);

        // Assert
        result.Should().NotBeNull();
        result.Id.Should().BeGreaterThan(0);
        result.CreatedAt.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(5));
        result.UpdatedAt.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(5));

        // Verify in database
        var dbProduct = await _context.Products.FindAsync(result.Id);
        dbProduct.Should().NotBeNull();
        dbProduct!.Name.Should().Be("New Product");
    }

    [Fact]
    public async Task AddAsync_WithNullProduct_ShouldThrowArgumentNullException()
    {
        // Act & Assert
        await _repository.Invoking(r => r.AddAsync(null!))
            .Should().ThrowAsync<ArgumentNullException>();
    }

    [Fact]
    public async Task UpdateAsync_WithValidProduct_ShouldUpdateSuccessfully()
    {
        // Arrange
        var product = new Product
        {
            Name = "Original Product",
            SKU = "ORIG001",
            Quantity = 5,
            Price = 10.00m
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        // Detach to simulate fresh retrieval
        _context.Entry(product).State = EntityState.Detached;

        var updatedProduct = new Product
        {
            Id = product.Id,
            Name = "Updated Product",
            SKU = "UPDATED001",
            Quantity = 15,
            Price = 25.00m,
            CreatedAt = product.CreatedAt
        };

        // Act
        var result = await _repository.UpdateAsync(updatedProduct);

        // Assert
        result.Should().NotBeNull();
        result.Name.Should().Be("Updated Product");
        result.SKU.Should().Be("UPDATED001");
        result.Quantity.Should().Be(15);
        result.Price.Should().Be(25.00m);
        result.UpdatedAt.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(5));
    }

    [Fact]
    public async Task DeleteAsync_WithValidId_ShouldDeleteSuccessfully()
    {
        // Arrange
        var product = new Product
        {
            Name = "Delete Test Product",
            SKU = "DELETE001",
            Quantity = 3,
            Price = 8.50m
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();
        var productId = product.Id;

        // Act
        var result = await _repository.DeleteAsync(productId);

        // Assert
        result.Should().BeTrue();

        var deletedProduct = await _context.Products.FindAsync(productId);
        deletedProduct.Should().BeNull();
    }

    [Fact]
    public async Task DeleteAsync_WithInvalidId_ShouldReturnFalse()
    {
        // Act
        var result = await _repository.DeleteAsync(999);

        // Assert
        result.Should().BeFalse();
    }

    [Fact]
    public async Task ExistsAsync_WithValidId_ShouldReturnTrue()
    {
        // Arrange
        var product = new Product
        {
            Name = "Exists Test Product",
            SKU = "EXISTS001",
            Quantity = 1,
            Price = 1.00m
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        // Act
        var result = await _repository.ExistsAsync(product.Id);

        // Assert
        result.Should().BeTrue();
    }

    [Fact]
    public async Task ExistsAsync_WithInvalidId_ShouldReturnFalse()
    {
        // Act
        var result = await _repository.ExistsAsync(999);

        // Assert
        result.Should().BeFalse();
    }

    [Fact]
    public async Task SkuExistsAsync_WithExistingSku_ShouldReturnTrue()
    {
        // Arrange
        var product = new Product
        {
            Name = "SKU Exists Test",
            SKU = "SKUEXISTS001",
            Quantity = 2,
            Price = 5.00m
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        // Act
        var result = await _repository.SkuExistsAsync("SKUEXISTS001");

        // Assert
        result.Should().BeTrue();
    }

    [Fact]
    public async Task SkuExistsAsync_WithExcludedId_ShouldReturnFalse()
    {
        // Arrange
        var product = new Product
        {
            Name = "SKU Exclude Test",
            SKU = "SKUEXCLUDE001",
            Quantity = 2,
            Price = 5.00m
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        // Act - Exclude the product's own ID
        var result = await _repository.SkuExistsAsync("SKUEXCLUDE001", product.Id);

        // Assert
        result.Should().BeFalse();
    }

    [Fact]
    public async Task CountAsync_ShouldReturnCorrectCount()
    {
        // Arrange - Add 2 more products (1 seed data already exists)
        var products = new[]
        {
            new Product { Name = "Count Test 1", SKU = "COUNT001", Quantity = 1, Price = 1.00m },
            new Product { Name = "Count Test 2", SKU = "COUNT002", Quantity = 2, Price = 2.00m }
        };

        await _context.Products.AddRangeAsync(products);
        await _context.SaveChangesAsync();

        // Act
        var count = await _repository.CountAsync();

        // Assert
        count.Should().Be(3); // 2 + 1 seed data
    }

    [Fact]
    public void Dispose_ShouldDisposeContextProperly()
    {
        // Arrange
        var repository = new ProductRepository(_context, _logger);

        // Act
        repository.Dispose();

        // Assert - Should not throw when disposing
        repository.Invoking(r => r.Dispose()).Should().NotThrow();
    }

    [Fact]
    public async Task Repository_DatabaseConnectionHandling_ShouldNotLeakMemory()
    {
        // This test verifies proper disposal and connection management
        var initialMemory = GC.GetTotalMemory(false);

        // Create multiple repositories and perform operations
        for (int i = 0; i < 10; i++)
        {
            using var tempContext = new InventoryDbContext(
                new DbContextOptionsBuilder<InventoryDbContext>()
                    .UseInMemoryDatabase($"temp_{i}")
                    .Options);

            using var tempRepository = new ProductRepository(tempContext, _logger);

            await tempRepository.AddAsync(new Product
            {
                Name = $"Temp Product {i}",
                SKU = $"TEMP{i:000}",
                Quantity = i,
                Price = i * 1.5m
            });
        }

        // Force garbage collection
        GC.Collect();
        GC.WaitForPendingFinalizers();
        GC.Collect();

        var finalMemory = GC.GetTotalMemory(false);

        // Memory should not have increased significantly (allowing for some variance)
        var memoryIncrease = finalMemory - initialMemory;
        memoryIncrease.Should().BeLessThan(1024 * 1024); // Less than 1MB increase
    }

    public void Dispose()
    {
        if (!_disposed)
        {
            _repository?.Dispose();
            _context?.Dispose();
            _disposed = true;
        }
    }
}