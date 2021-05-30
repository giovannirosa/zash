from modules.behavior.configuration import ConfigurationComponent
from models_zash import Request


class OntologyComponent:
    def __init__(self, configuration_component: ConfigurationComponent):
        self.configuration_component = configuration_component

    # common ontologies like:
    #   - critical devices:
    #       - visitor cannot even visualize
    #       - kids can only visualize
    #       - adults can only visualize and control
    #       - admins can visualize, control and manage
    #   - non-critical devices:
    #       - visitor and kids can visualize and control
    #       - adults and admins can visualize, control and manage
    def verify_ontology(self, req: Request):
        print("Ontology Component")
        print("Verify User Level {} with the Action {} on the device class {}".format(
            req.user.user_level, req.action, req.device.device_class))
        compatible = True
        print(self.configuration_component.ontologies)
        capabilities = next((ontology.capabilities for ontology in self.configuration_component.ontologies if ontology.user_level ==
                                   req.user.user_level and ontology.device_class == req.device.device_class), [])
        print(capabilities)
        if req.action in capabilities:
            compatible = True
        else:
            compatible = False
        str_result = 'compatible'
        if not compatible:
            str_result = 'incompatible'
        print("User level {} is {} with the Action {} on the device class {}".format(
            req.user.user_level, str_result, req.action, req.device.device_class))
        return compatible