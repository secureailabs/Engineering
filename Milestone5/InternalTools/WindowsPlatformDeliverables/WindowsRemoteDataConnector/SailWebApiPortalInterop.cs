using System;
using System.Runtime.InteropServices;

public class SailWebApiPortalInterop
{
    #region Session Management Functions

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

    /// <summary>
    /// 
    /// </summary>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl )]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GetSailWebApiPortalImpostorEosb();

    /// <summary>
    /// 
    /// </summary>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl )]
    static extern public uint LoadDigitalContracts();

    /// <summary>
    /// 
    /// </summary>
    /// <param name="index"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl )]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GetDigitalContractIdentifierAtIndex(uint index);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="digitalContractIdentifier"></param>
    /// <param name="propertyName"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl )]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GetDigitalContractProperty(string digitalContractIdentifier, string propertyName);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="virtualMachineIpAddress"></param>
    /// <param name="base64EncodedInstallationPackage"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl )]
    static extern public bool UploadInstallationPackageToVirtualMachine(string virtualMachineIpAddress, string base64EncodedInstallationPackage);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="nameOfVirtualMachine"></param>
    /// <param name="ipAddressOfVirtualMachine"></param>
    /// <param name="virtualMachineIdentifier"></param>
    /// <param name="clusterIdentifier"></param>
    /// <param name="digitalContractIdentifier"></param>
    /// <param name="datasetIdentifier"></param>
    /// <param name="rootOfTrustDomainIdentifier"></param>
    /// <param name="computationalDomainIdentifier"></param>
    /// <param name="dataConnectorDomainIdentifier"></param>
    /// <param name="ipAddressOfSailWebApiPortal"></param>
    /// <param name="base64EncodedDataset"></param>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl )]
    static extern public bool UploadInitializationParametersToVirtualMachine(string nameOfVirtualMachine, string ipAddressOfVirtualMachine, string virtualMachineIdentifier, string clusterIdentifier, string digitalContractIdentifier, string datasetIdentifier, string rootOfTrustDomainIdentifier, string computationalDomainIdentifier, string dataConnectorDomainIdentifier, string ipAddressOfSailWebApiPortal, string base64EncodedDataset);

    /// <summary>
    /// 
    /// </summary>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public int RemoteDataConnectorHeartbeat();

    /// <summary>
    /// 
    /// </summary>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public int RemoteDataConnectorUpdateDatasets();

    /// <summary>
    /// 
    /// </summary>
    /// <param name="datasetFile"></param>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl )]
    static extern public void RemoteDataConnectorAddDataset(string datasetFile);

    /// <summary>
    /// 
    /// </summary>
    /// <param name="datasetFile"></param>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern public void RemoteDataConnectorRemoveDataset(string datasetFile);

    /// <summary>
    /// 
    /// </summary>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl )]
    static extern public uint GetExceptionCount();

    /// <summary>
    /// 
    /// </summary>
    /// <returns></returns>
    [DllImport("SailSupportLibrary.dll", CallingConvention = CallingConvention.Cdecl )]
    [return: MarshalAs(UnmanagedType.BStr)]
    static extern public string GetNextException();
}