openai_functions = [
    {
        "name": "create_website",
        "description": "create a website using a list of blocks which are appropriate for this website. Only blocks releveant for user website should be included in list",
        "parameters": {
            "type": "object",
            "properties": {
                "blocks": {
                    "type": "array",
                    "description": "Array of blocks of which website will be made. Should only contain relevant blocks for this particular website. Order of blocks should be how they should appear in website",
                    "items": {
                        "type": "string",
                        "enum": ["header", "intro", "custom_links", "services", "text", "gallery", "products", "testimonials", "contact_form", "social_links"],
                        "description": "A block which occupies the full horizontal width of website"
                    }
                }
            },
            "required": ["blocks"]
        }
    },
    {
        "name": "search_email",
        "description": "search all the emails of the user to find specific email that user wants",
        "parameters": {
            "type": "object",
            "properties": {
                "from_email": {
                    "type": "string",
                    "description": "from email address which can be userd to filter all emails sent by a certain email address",
                },
                "words": {
                    "type": "string",
                    "description": "text which should be there in email subject or body",
                }
            },
            "required": ["from_email", "words"],
        },
    },
    {
        "name": "change_name",
        "description": "Change the name of the user to new specified name",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "new name of the user",
                },
            },
            "required": ["name"],
        },
    },
    {
        "name": "create_folder",
        "description": "create a new folder for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_name": {
                    "type": "string",
                    "description": "folder name which user wants to create",
                },
            },
            "required": ["folder_name"],
        },
    },
    {
        "name": "add_rule_move_to_folder",
        "description": "add a new filter or rule which helps user to to filter his incoming mails. For example move mails coming from certain email to some folder",
        "parameters": {
            "type": "object",
            "properties": {
                "rule_name": {
                    "type": "string",
                    "description": "name of the rule user wants to create",
                },
                "from_email": {
                    "type": "string",
                    "description": "a valid emaill address for the the filter being created. Filter will be applied on all the mail coming from this email",
                },
                "folder_name": {
                    "type": "string",
                    "description": "folder name to which mails need to be moved to based on the filter",
                }
            },
            "required": ["rule_name", "from_email", "folder_name"],
        }
    }
]
