SCN_COMPONENTS= \
VirtualMachine/BaseVmImageInit \
VirtualMachine/CommunicationPortal \
VirtualMachine/DataDomainProcess \
VirtualMachine/InitializerProcess \
VirtualMachine/JobEngine \
VirtualMachine/PrivacySentinel \
VirtualMachine/RootOfTrustProcess \
VirtualMachine/SignalTerminationProcess

SCN_PACKAGE= \
Binary/BaseVmImageInit \
Binary/CommunicationPortal \
Binary/DataDomainProcess \
Binary/InitializerProcess \
Binary/JobEngine \
Binary/PrivacySentinel \
Binary/RootOfTrustProcess \
Binary/SignalTerminationProcess

SCN_BINARIES=$(SCN_COMPONENTS:VirtualMachine/%=Binary/%)

Binary/%: VirtualMachine/%
	@cd $^ && make all -j

scn_componenets: $(SCN_BINARIES)

package_securecomputationnode: $(SCN_BINARIES)
	@tar -czvf Binary/SecureComputationNode.tar.gz $(SCN_BINARIES)
