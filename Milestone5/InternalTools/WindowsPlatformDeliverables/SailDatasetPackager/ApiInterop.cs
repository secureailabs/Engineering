using System;
using System.Runtime.InteropServices;

public class ApiInterop
{
    #region Miscellaneous Support Functions

    /// <summary>
    /// 
    /// </summary>
    /// <param name="value"></param>
    /// <param name="caseSensitive"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public ulong Get64BitHashOfString(string value, bool caseSensitive);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="identifierType"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GenerateIdentifier(uint identifierType);

    #endregion

    #region Table Packages Support Functions

    /// <summary>
    /// 
    /// </summary>
    /// <param name="c_szTargetFilename"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public uint AddTablePackageFromFile(string c_szTargetFilename);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="tableIndex"></param>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public void RemoveTablePackageByIndex(uint tableIndex);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="tableIndex"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GetTablePackageIdentifierByIndex(uint tableIndex);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="tableIndex"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GetTablePackageTitleByIndex(uint tableIndex);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="tableIndex"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GetTablePackageDescriptionByIndex(uint tableIndex);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="tableIndex"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GetTablePackageFilenameByIndex(uint tableIndex);

    #endregion

    #region Dataset Packaging and Publishing Support Functions

    /// <summary>
    /// 
    /// </summary>
    /// <param name="datasetFilename"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public bool GenerateDataset(string datasetFilename, string datasetIdentifier, string datasetTitle, string datasetDescription, string datasetTags, string datasetFamilyIdentifier);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="datasetFilename"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public bool PublishDataset(string datasetFilename);

    #endregion

    #region JsonParser Test Functions

    /// <summary>
    /// 
    /// </summary>
    /// <param name="jsonString"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string TestConvertJsonStringToStructuredBuffer(string jsonString);

    /// <summary>
    /// 
    /// </summary>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string TestConvertStructuredBufferToStandardJson();

    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string TestConvertStructuredBufferToStronglyTypedJson();

    #endregion

    #region Dataset Family Support Functions

    /// <summary>
    /// 
    /// </summary>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public bool UpdateDatasetFamilyInformation();

    /// <summary>
    /// 
    /// </summary>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GetListOfDatasetFamilyIdentifiers();

    /// <summary>
    /// 
    /// </summary>
    /// <param name="datasetFamilyIdentifier"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GetDatasetFamilyTitle(string datasetFamilyIdentifier);

    #endregion

    #region Session Management Support Functions

    /// <summary>
    /// 
    /// </summary>
    /// <param name="username"></param>
    /// <param name="password"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public bool Login(string sailPlatformIpAddress, string username, string password);

    /// <summary>
    ///     
    /// </summary>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public bool Logout();

    /// <summary>
    /// 
    /// </summary>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public bool IsLoggedOn();

    #endregion

    #region Exception Reporting Support Functions

    /// <summary>
    /// 
    /// </summary>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public uint GetExceptionCount();

    /// <summary>
    /// 
    /// </summary>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GetNextException();

    #endregion
}