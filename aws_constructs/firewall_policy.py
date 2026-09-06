from aws_cdk import aws_networkfirewall as nfw
from constructs import Construct

class FirewallPolicyConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        firewall_policy_name: str,
    ) -> None:
        super().__init__(scope, construct_id)

        self.policy = nfw.CfnFirewallPolicy(
            self,
            "FirewallPolicy",
            firewall_policy_name=firewall_policy_name,

            firewall_policy=nfw.CfnFirewallPolicy.FirewallPolicyProperty(
                stateless_default_actions=[
                    "aws:forward_to_sfe"
                ],

                stateless_fragment_default_actions=[
                    "aws:forward_to_sfe"
                ],

                stateful_engine_options=nfw.CfnFirewallPolicy.StatefulEngineOptionsProperty(
                    rule_order="STRICT_ORDER"
                ),

                stateful_default_actions=[
                    "aws:drop_established",
                    "aws:alert_established"
                ],
            )
        )