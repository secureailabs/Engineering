#  Install dot net core
Follow the instructions from:
https://learn.microsoft.com/en-us/dotnet/core/install/linux-scripted-manual#scripted-install


# Create a new project
```bash
dotnet new console -o DatasetTool -f net6.0
```

# Run the project
```bash
dotnet run
```

# Build the project
```bash
dotnet build
```

# Generate a gitignore file
```bash
dotnet new gitignore
```

# Add a reference to a nuget package
```bash
dotnet add package Microsoft.Extensions.Configuration
```
