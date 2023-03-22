dotnet publish -c Release -r win-x64

# Create a folder for the release
Set-Variable -Name dir_name -Value "SAILDatasetUpload-win-x64"
Set-Variable -Name output_name -Value "SAILDatasetUpload-win-x64.zip"
if (Test-Path $dir_name) {
    Remove-Item -Path $dir_name -Recurse -Force
}
if (Test-Path $output_name) {
    Remove-Item -Path $output_name -Force
}

mkdir $dir_name

Copy-Item .\bin\Release\net6.0\win-x64\publish\* $dir_name -Recurse

Copy-Item .\SampleData $dir_name -Recurse

# Zip the release
Compress-Archive -Path $dir_name\* -DestinationPath $output_name
