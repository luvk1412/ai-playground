website_json_format = {
    "header": {
        "title": "This should be title of the web site. Kind of logo. Should be short",
        "image_search_prompt": "short two word description of brand logo"
    },
    "intro": {
        "heading": "this should be heading for page",
        "description": "this should be 2-3 line description about the business",
        "button_label": "Label text of button"
    },
    "custom_links": {
        "links": [
            {
                "button_label": "Label for the button",
                "button_icon": "One of the 12 icons: (need to type all icons here)"
            }
        ]
    },
    "services_section": {
        "heading": "",
        "button_label": "Each service will have a button on ui and this label will be used for all services, For ex: Book this Service/Book",
        "currency": "currency unit to use one of USD, EUR, GBP",
        "services": [
            {
                "name": "name of the service",
                "description": "service desc",
                "price": "integer value of price in unit defined above",
                "image_search_prompt": "short two word description for above service"
            }
        ]
    },
    "text": {
        "heading": "",
        "description": "",
        "button_label": ""
    },
    "gallery_section": {
        "heading": "",
        "button_label": "",
        "images": [
            {
                "image_description": "",
                "image_search_prompt": "short two word descrioption of above image"

            }
        ]
    },
    "product_section": {
        "heading": "",
        "main_button_label": "Label for main button show to right of Heading, For example: Shope all",
        "button_label": "Each product will have a button on ui and this label will be used for all products, For ex: Buy/Buy Now",
        "currency": "currency unit to use one of USD, EUR, GBP",
        "products": [
            {
                "name": "",
                "price": "integer value of price in unit defined above",
                "image_search_prompt": "short two word description for above product"
            }
        ]
    },
    "testimonial_section": {
        "heading": "Headin of the testimonial section",
        "testimonials": [
            {
                "quote": "Reviw given by user. Should be 3-5 lines.",
                "written_by": "name of a person",
                "designation": "",
                "gender": "male or female"
            }
        ]
    },
    "contact_form": {
        "heading": "heading of the contact form"
    },
    "social_links": {
        "links": [
            {
                "type": "facebook/linkedin/twitter/tiktok",
                "link": ""
            }
        ]
    }
}


functions = [
    {
        "name": "change_website",
        "description": "This function should be called when user explicitly asks to change the website content. This should not be called when asked for suggestions or for ui changes as this can only change content",
        "parameters": {
            "type": "object",
            "properties": {
                "changes_to_made": {
                    "type": "string",
                    "description": "A prompt which describes what changes should be made to the website",
                }
            },
            "required": ["changes_to_make"],
        },
    }
]