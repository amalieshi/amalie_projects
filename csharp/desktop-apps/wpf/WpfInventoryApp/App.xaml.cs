using System;
using System.Windows;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using WpfInventoryApp.Data;
using WpfInventoryApp.Repositories;
using WpfInventoryApp.ViewModels;
using WpfInventoryApp.Views;

namespace WpfInventoryApp;

public partial class App : Application
{
    private ServiceProvider? _serviceProvider;
    private IConfiguration? _configuration;

    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        try
        {
            ConfigureServices();
            InitializeDatabase();
            ShowMainWindow();
        }
        catch (Exception ex)
        {
            MessageBox.Show($"Application startup failed: {ex.Message}", "Startup Error",
                MessageBoxButton.OK, MessageBoxImage.Error);
            Shutdown(1);
        }
    }

    private void ConfigureServices()
    {
        // Build configuration
        _configuration = new ConfigurationBuilder()
            .SetBasePath(AppDomain.CurrentDomain.BaseDirectory)
            .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
            .AddEnvironmentVariables()
            .Build();

        // Configure services
        var services = new ServiceCollection();

        // Configuration
        services.AddSingleton<IConfiguration>(_configuration);

        // Logging
        services.AddLogging(builder =>
        {
            builder.SetMinimumLevel(LogLevel.Information);
            builder.AddConsole();
            builder.AddDebug();
        });

        // Database
        var connectionString = _configuration.GetConnectionString("DefaultConnection")
            ?? Environment.GetEnvironmentVariable("INVENTORY_DB_CONNECTION")
            ?? "Data Source=inventory.db;Cache=Shared";

        services.AddDbContext<InventoryDbContext>(options =>
        {
            options.UseSqlite(connectionString);
            options.EnableSensitiveDataLogging(false);
            options.EnableServiceProviderCaching();
        });

        // Repository
        services.AddScoped<IProductRepository, ProductRepository>();

        // ViewModels
        services.AddTransient<MainViewModel>();

        // Views
        services.AddTransient<MainWindow>();

        _serviceProvider = services.BuildServiceProvider();
    }

    private void InitializeDatabase()
    {
        using var scope = _serviceProvider!.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<InventoryDbContext>();
        var logger = scope.ServiceProvider.GetRequiredService<ILogger<App>>();

        try
        {
            logger.LogInformation("Initializing database...");
            context.Database.EnsureCreated();
            logger.LogInformation("Database initialized successfully");
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Failed to initialize database");
            throw;
        }
    }

    private void ShowMainWindow()
    {
        var mainWindow = _serviceProvider!.GetRequiredService<MainWindow>();
        var viewModel = _serviceProvider!.GetRequiredService<MainViewModel>();

        mainWindow.DataContext = viewModel;
        mainWindow.Show();

        MainWindow = mainWindow;
    }

    protected override void OnExit(ExitEventArgs e)
    {
        _serviceProvider?.Dispose();
        base.OnExit(e);
    }
}