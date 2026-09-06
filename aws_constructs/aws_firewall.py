from aws_cdk import aws_networkfirewall as nfw
from constructs import Construct

class NetworkFirewallConstruct(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        firewall_name: str,
        firewall_policy_arn: str,
        firewall_subnet_ids: list[str],
        alert_log_group_name: str,
        flow_log_group_name: str,
        vpc_id: str,
        tags: Optional[Dict[str, str]] = None, 
    ) -> None:
        super().__init__(scope, construct_id)

        firewall_tags = []

        if tags:
            firewall_tags.extend(
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in firewall_tags.items()
            )

        self.firewall = nfw.CfnFirewall(
            self,
            "NetworkFirewall",
            firewall_name=firewall_name,
            firewall_policy_arn=firewall_policy_arn,
            subnet_mappings=[
                nfw.CfnFirewall.SubnetMappingProperty(
                    subnet_id=subnet_id
                )
                for subnet_id in firewall_subnet_ids
            ],
            vpc_id=vpc_id,
            tags= firewall_tags
        )

        # Logging configuration
        self.logging_configuration = nfw.CfnLoggingConfiguration(
            self,
            "FirewallLoggingConfiguration",
            firewall_arn=self.firewall.attr_firewall_arn,
            logging_configuration=nfw.CfnLoggingConfiguration.LoggingConfigurationProperty(
                log_destination_configs=[
                    nfw.CfnLoggingConfiguration.LogDestinationConfigProperty(
                        log_destination_type="CloudWatchLogs",
                        log_type="ALERT",
                        log_destination={
                            "logGroup": alert_log_group_name
                        }
                    ),  

                    nfw.CfnLoggingConfiguration.LogDestinationConfigProperty(
                        log_destination_type="CloudWatchLogs",
                        log_type="FLOW",
                        log_destination={
                            "logGroup": flow_log_group_name
                        }
                    )
                ]
            )
        )