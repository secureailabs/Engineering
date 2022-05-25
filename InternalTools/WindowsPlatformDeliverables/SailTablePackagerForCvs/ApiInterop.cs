using System;
using System.Runtime.InteropServices;

public class ApiInterop
{
    /// <summary>
    /// 
    /// </summary>
    /// <returns></returns>
    [DllImport("kernel32")]
    static extern public int AttachConsole(uint processIdentifier);

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

    /// <summary>
    /// 
    /// </summary>
    /// <param name="filename"></param>
    /// <param name="filesize"></param>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public void OpenTablePackageFileForWriting(string filename, long filesize);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="columnIdentifier"></param>
    /// <param name="columnName"></param>
    /// <param name="columnDescription"></param>
    /// <param name="columnTags"></param>
    /// <param name="columnUnits"></param>
    /// <param name="columnType"></param>
    /// <param name="columnUnitCategories"></param>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public void AddColumnToTablePackageFile(string columnIdentifier, string columnName, string columnDescription, string columnTags, string columnUnits, string columnType, string columnUnitCategories);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="filename"></param>
    /// <param name="filesize"></param>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public void AddRecordToTablePackageFile(string rawRecord);

    /// <summary>
    /// 
    /// </summary>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public void CompleteTablePackageFile(string tableIdentifier, string tableTitle, string tableDescription, string tableTags, int numberOfColumns, int numberOfRows);
}