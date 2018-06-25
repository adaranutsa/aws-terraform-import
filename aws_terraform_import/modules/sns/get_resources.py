class SnsResource:
    """Class object to store SNS resources
    
    This class will store only SNS information that
    is needed by the terraform module.
    """
    
    def __init__(self, name):
        
        # SNS Topic Name
        self.name = name
        
        # SNS Topic Display Name
        self.display_name = ''
        
        # SNS Topic ARN
        self.topic_arn = ''
        
        # SNS Subscription ARN
        self.subscription_arn = ''
        
        # AWS Account ID
        self.account_id = ''
        
        # SNS Topic Policy
        self.policy = ''
        
        # SNS Topic Delivery Policy
        self.delivery_policy = ''
        
        