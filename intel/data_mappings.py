"""We use these dictionaries to map Intel's key on the website to our key in the database.

These are used in intel/scrape_intel_ark.py.
"""

from __future__ import annotations

# TODO(TheLovinator): #47 Check so we don't have duplicates.
# https://github.com/TheLovinator1/panso.se/issues/47

mapping: dict[str, str] = {
    "ProductGroup": "product_collection",
    "MarketSegment": "vertical_segment",
    "ProcessorNumber": "processor_number",
    "Lithography": "lithography",
    "CertifiedUseConditions": "use_conditions",
    "Cache": "cache",
    "Bus": "bus_speed",
    "TotalL2Cache": "l2_cache",
    "StatusCodeText": "marketing_status",
    "BornOnDate": "launch_date",
    "ProductBriefUrl": "product_brief_url",
    "DatasheetUrl": "datasheet",
    "ServicingStatus": "servicing_status",
    "MemoryTypes": "memory_types",
    "ScalableSockets": "scalability",
    "PCIExpressRevision": "pci_express_revision",
    "MicroprocessorPCIeRevision": "microprocessor_pcie_revision",
    "ChipsetPCHPCIeRevision": "chipset_pch_pcie_revision",
    "DMIRevision": "direct_media_interface_revision",
    "USBRevision": "usb_revision",
    "USBConfigurationDescription": "usb_configuration",
    "UART": "uart",
    "SocketsSupported": "sockets_supported",
    "PackageCarrier": "package_carrier",
    "PackageSize": "package_size",
    "OperatingTemperature": "operating_temperature_range",
    "ThermalSolutionSpecification": "thermal_solution_specification",
    "TBTVersion": "turbo_boost_technology",
    "InstructionSet": "instruction_set",
    "InstructionSetExtensions": "instruction_set_extensions",
    "DeepLearningBoostVersion": "deep_learning_boost_version",
    "ProcessorGraphicsModelId": "processor_graphics",
    "GraphicsOutput": "graphics_output",
    "GraphicsMaxResolutionHDMI": "max_resolution_hdmi",
    "GraphicsMaxResolutionDP": "max_resolution_dp",
    "GraphicsMaxResolutionIFP": "max_resolution_edp_integrated_flat_panel",
    "GraphicsDirectXSupport": "directx_support",
    "GraphicsOpenGLSupport": "opengl_support",
    "GraphicsOpenCLSupport": "opencl_support",
    "MultiFormatCodecEngines": "multi_format_codec_engines",
    "GraphicsDeviceId": "device_id",
    "Graphics4KSupportLevel": "_4k_support",
    "NetworkInterfaces": "network_interfaces",
}

float_bois: dict[str, str] = {"MipiSoundwireVersion": "mipi_soundwire_version"}

temp_bois: dict[str, str] = {
    "DigitalThermalSensorTemperatureMax": "digital_thermal_sensor_temperature_max",
    "OperatingTemperatureMax": "operating_temperature_max",
    "OperatingTemperatureMin": "operating_temperature_min",
    "TCase": "t_case",
}
bandwidth_bois: dict[str, str] = {"MaxMemoryBandwidth": "max_memory_bandwidth"}

byte_bois: dict[str, str] = {
    "MaxMem": "max_memory_size",
    "MaxEncSizeSupportIntelSGX": "maximum_enclave_size_for_sgx",
}

bool_bois: dict[str, str] = {
    "Embedded": "embedded_options_available",
    "OptaneDCPersistentMemoryVersion": "optane_supported",
    "ECCMemory": "ecc_memory_supported",
    "IntelThunderbolt4": "thunderbolt_4_support",
    "IntegratedIDE": "integrated_ide",
    "GeneralPurposeIO": "general_purpose_io",
    "IntegratedLAN": "integrated_lan",
    "ResourceDirectorTechVersion": "resource_director_technology",
    "OptaneMemorySupport": "optane_supported",
    "HyperThreading": "hyper_threading_technology",
    "EM64": "_64_bit",
    "AVX512FusedMultiplyAddUnits": "avx_512_fma_units",
    "SpeedstepTechnology": "enhanced_speedstep_technology",
    "ThermalMonitoring2Indicator": "thermal_monitoring_technologies",
    "QuickAssistTechnology": "integrated_quick_assist_technology",
    "VolumeManagementDeviceVersion": "volume_management_device",
    "TimeCoordinatedComputing": "time_coordinated_computing",
    "GaussianNeuralAcceleratorVersion": "gaussian_neural_accelerator",
    "IntelThreadDirector": "thread_director",
    "ImageProcessingUnitVersion": "image_processing_unit",
    "IntelSmartSoundTechnology": "smart_sound_technology",
    "IntelWakeonVoice": "wake_on_voice",
    "IntelHighDefinitionAudio": "high_definition_audio",
    "AdaptixTechVersion": "adaptix_technology",
    "SpeedShiftTechVersion": "speed_shift_technology",
    "TurboBoostMaxTechVersion": "turbo_boost_max_technology_3_0",
    "FlexMemoryTechnology": "flex_memory_access",
    "ThermalVelocityBoostVersion": "thermal_velocity_boost",
    "HaltState": "idle_states",
    "AdaptiveBoostTechVesion": "adaptive_boost_technology",
    "TransactionalSynchronizationExtensionVersion": "transactional_synchronization_extensions",
    "DemandBasedSwitching": "demand_based_switching",
    "IdentityProtectionTechVersion": "identity_protection_technology",
    "IntelQAssistSWAccel": "quick_assist_software_acceleration",
    "IntelTotalMemoryEncryption": "total_memory_encryption",
    "AESTech": "aes_new_instructions",
    "SoftwareGuardExtensions": "software_guard_extensions",
    "TXT": "trusted_execution_technology",
    "ExecuteDisable": "execute_disable_bit",
    "DeviceProtectionTechBootGuardVersion": "boot_guard",
    "IntelPlatformFWResSupport": "platform_firmware_resilience",
    "IntelCryptoAcceleration": "crypto_acceleration",
    "VTX": "virtualization_technology",
    "VTD": "virtualization_technology_for_directed_io",
    "VProTechnologyOptions": "vpro_eligibility",
    "ThreatDetectTech": "threat_detection_technology",
    "ActiveManagementTech": "active_management_technology",
    "StandardManageability": "standard_manageability",
    "RemotePlatformErase": "remote_platform_erase",
    "OneClickRecovery": "one_click_recovery",
    "IntelHardwareShield": "hardware_shield",
    "IntelControlFlowEnforcementTechnology": "control_flow_enforcement_technology",
    "IntelTotalMemoryEncryptionWithMultikey": "total_memory_encryption_multi_key",
    "SecureKeyTechVersion": "secure_key",
    "OSGuardTechVersion": "os_guard",
    "ModeBasedExecutionControlVersion": "mode_based_execute_control",
    "StableImagePlatformProgramVersion": "stable_image_platform_program",
    "VTRP": "virtualization_technology_with_redirect_protection",
    "ExtendedPageTables": "virtualization_technology_with_extended_page_tables",
    "QuickSyncVideo": "intel_quick_sync_video",
    "CVTHD": "intel_clear_video_hd_technology",
    "InTru3D": "intel_in_tru_3d_technology",
    "ClearVideoTechnology": "intel_clear_video_technology",
}


watt_bois: dict[str, str] = {
    "MaxTDP": "tdp",
    "ProcessorBasePower": "processor_base_power",
    "MaxTurboPower": "max_turbo_power",
    "AssuredPowerMin": "min_assured_power",
    "AssuredPowerMax": "max_assured_power",
}

hertz_bois: dict[str, str] = {
    "ClockSpeedMax": "max_turbo_frequency",
    "ClockSpeed": "base_frequency",
    "TurboBoostMaxTechMaxFreq": "turbo_boost_max_technology_3_0_frequency",
    "PCoreTurboFreq": "single_performance_core_turbo_frequency",
    "ECoreTurboFreq": "single_efficiency_core_turbo_frequency",
    "PCoreBaseFreq": "p_core_base_frequency",
    "ECoreBaseFreq": "e_core_base_frequency",
    "ThermalVelocityBoostFreq": "thermal_velocity_boost_frequency",
    "TurboBoostTech2MaxFreq": "turbo_boost_2_0_frequency",
    "MemoryMaxSpeedMhz": "max_memory_speed",
    "GraphicsMaxFreq": "graphics_max_dynamic_frequency",
    "GraphicsFreq": "graphics_base_frequency",
}

int_bois: dict[str, str] = {
    "CoreCount": "total_cores",
    "PerfCoreCount": "performance_cores",
    "ThreadCount": "total_threads",
    "EffCoreCount": "efficiency_cores",
    "UltraPathInterconnectLinks": "upi_links",
    "BusNumPorts": "number_of_qpi_links",
    "NumMemoryChannels": "max_number_of_memory_channels",
    "NumPCIExpressPorts": "max_amount_of_pci_express_lanes",
    "MaxDMILanesCount": "max_amount_of_direct_media_interface_lanes",
    "NumUSBPorts": "number_of_usb_ports",
    "NumSATAPorts": "number_of_sata_ports",
    "SATA6PortCount": "number_of_sata_6_0_ports",
    "MaxCPUs": "max_cpu_configuration",
    "GraphicsExecutionUnits": "execution_units",
    "NumDisplaysSupported": "number_of_displays_supported",
}

bit_bois: dict[str, str] = {
    "PhysicalAddressExtension": "physical_address_extensions",
}
