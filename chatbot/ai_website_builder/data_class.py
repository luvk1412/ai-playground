class UserWebsiteInput:
    def __init__(self, data):
        self.name = data.get('name')
        self.desc = data.get('desc')

        self.landing_page = data.get('landing_page')

        self.product_or_service = data.get('product_or_service')
        self.value_prop = data.get('value_prop')
        self.features = data.get('features')
        self.benefits = data.get('benefits')
        self.target_audience = data.get('target_audience')
        self.tone_and_voice = data.get('tone_and_voice')

    def validate(self):
        required_attrs = ['name', 'desc']

        if self.landing_page:
            required_attrs.extend(['product_or_service', 'value_prop', 'features', 'benefits', 'target_audience', 'tone_and_voice'])

        for attr in required_attrs:
            value = getattr(self, attr, None)
            if not isinstance(value, str):
                raise ValueError(f"Expected {attr} to be a string, got {type(value).__name__}")

    def to_qna_string(self):
        qna_string = f"Business Name: {self.name}\nBusiness Description: {self.desc}\n"
        if self.landing_page:
            qna_string += f"Product or Service: {self.product_or_service}\n"
            qna_string += f"Value Proposition: {self.value_prop}\n"
            qna_string += f"Features: {self.features}\n"
            qna_string += f"Benefits: {self.benefits}\n"
            qna_string += f"Target Audience: {self.target_audience}\n"
        return qna_string

