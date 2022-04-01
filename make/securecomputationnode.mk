SCN_COMPONENTS= \
VirtualMachine/CommunicationPortal \
VirtualMachine/DataDomainProcess \
VirtualMachine/InitializerProcess \
VirtualMachine/JobEngine \
VirtualMachine/PrivacySentinel \
VirtualMachine/RootOfTrustProcess \
VirtualMachine/SignalTerminationProcess

SCN_PACKAGE= \
Binary/CommunicationPortal \
Binary/DataDomainProcess \
Binary/InitializerProcess \
Binary/JobEngine \
Binary/PrivacySentinel.py \
Binary/PrivacySentinelPolicy.json \
Binary/RootOfTrustProcess \
Binary/SignalTerminationProcess

SCN_BINARIES=$(SCN_COMPONENTS:VirtualMachine/%=Binary/%)

Binary/%: VirtualMachine/%
	@make -C $^ all

scn_componenets: SharedCommonCode
	@make $(SCN_BINARIES)

package_securecomputationnode: scn_componenets
	@tar -czvf Binary/SecureComputationNode.tar.gz $(SCN_PACKAGE)
