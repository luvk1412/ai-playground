def convert_to_new_format(original_json):

    def site_defaults(data):
        defaults = {"isVisible": bool(data)}
        if isinstance(data, list):
            defaults['visibleItems'] = len(data)
        return defaults
    
    def get_data_json(data):
        return {
                "siteDefaults": site_defaults(data),
                "data": data
        }
    
    def get_data_json_nested(data):
        return {
                "siteDefaults": site_defaults(data),
                "data": {
                    "value": data
                }
        }

    def get_img_data_json(data):
        return {
                "siteDefaults": site_defaults(data),
                "data": {
                    "search_prompt": data,
                    "url": "to be filled from stock search"
                }
        }
    
    new_json = {
        "id": "T2",
        "key": "note sure",
        "displayName": "note sure",
        "version": 1,
        "blocks": []
    }

    def convert_section(key, template_key, order, version, data_converter):
        data = original_json.get(key, {})
        section = {
            "key": template_key,
            "order": order,
            "version": version,
            "siteDefaults": site_defaults(data=data),
            "layout": "v1/layout/" + template_key,
            "data": data_converter(data)
        }
        return section

    def convert_header(data):
        return {
            "title": get_data_json(data=data.get("title")),
            "logo_image": get_img_data_json(data=data.get("image_search_prompt"))
        }

    def convert_intro(data):
        return {
            "heading": get_data_json(data=data.get("heading")),
            "description": get_data_json(data=data.get("description")),
            "coverImage": get_img_data_json(data=data.get("image_search_prompt")),
            "mainButton": {
                "siteDefaults": site_defaults(data.get("button_label")),
                "data": {
                    "buttonLabel": get_data_json(data=data.get("button_label")),
                    "linkType": get_data_json_nested("customLink"),
                    "url": get_data_json("https://www.google.com")
                }
            }
        }
    
    def convert_custom_links(data):
        links_list = data.get("links", [])
        converted_links = []
        for link in links_list:
            converted_link = {
                "linkItem": {
                    "siteDefaults": site_defaults(link),
                    "data": {
                        "buttonLabel": get_data_json(data=link.get("button_label")),
                        "linkType": get_data_json_nested("customLink"),
                        "url": get_data_json("https://www.google.com"),
                        "icon": {
                            "siteDefaults": site_defaults(link.get("button_icon")),
                            "data": {
                                "label": "note sure",
                                "value": "note sure",
                                "icon": link.get("button_icon", "")
                            }
                        }
                    }
                }
            }
            converted_links.append(converted_link)
        
        return {
            "linksList": {
                "siteDefaults": site_defaults(links_list),
                "data": converted_links
            }
        }

    def convert_services_section(data):
        services_list = data.get("services", [])
        converted_services = []
        for service in services_list:
            converted_service = {
                "serviceItem": {
                    "siteDefaults": site_defaults(service),
                    "data": {
                        "heading": get_data_json(data=data.get("heading")),
                        "description": get_data_json(data=data.get("description")),
                        "image": get_img_data_json(data=data.get("image_search_prompt")),
                        "serviceButton": {
                            "siteDefaults": {"isVisible": True},
                            "data": {
                                "linkType": get_data_json_nested("customLink"),
                                "url": get_data_json("https://www.google.com")
                            }
                        },
                        "price": get_data_json(data=data.get("price")),
                    }
                }
            }
            converted_services.append(converted_service)
        
        return {
            "heading": get_data_json(data=data.get("heading")),
            "serviceList": get_data_json(data=services_list),
            "serviceDisplay": {
                "siteDefaults": {"isVisible": True},
                "data": {
                    "showButton": {
                        "siteDefaults": site_defaults(data.get("button_label")),
                        "data": {
                            "buttonLabel": get_data_json(data=data.get("button_label")),
                        }
                    },
                    "showPrice": {
                        "siteDefaults": site_defaults(data.get("currency")),
                        "data": {
                            "currency": get_data_json(data=data.get("currency"))
                        }
                    }
                }
            }
        }
    
    def convert_text(data):
        return {
            "heading": get_data_json(data.get("heading")),
            "description": get_data_json(data.get("description")),
            "buttonLabel": get_data_json(data.get("button_label")),
            "bookings": get_data_json("note sure")
        }

    def convert_gallery_section(data):
        images_list = data.get("images", [])
        converted_images = []
        for image in images_list:
            converted_image = {
                "galleryItem": {
                    "siteDefaults": site_defaults(image),
                    "data": {
                        "image": get_img_data_json(image.get("image_search_prompt")),
                        "description": get_data_json(image.get("image_description")),
                        "link": {
                            "siteDefaults": site_defaults(True),
                            "data": {
                                "linkType": get_data_json_nested("customLink"),
                                "url": get_data_json("https://www.google.com")
                            }
                        }
                    }
                }
            }
            converted_images.append(converted_image)
        
        return {
            "heading": get_data_json(data.get("heading")),
            "mainButton": {
                "siteDefaults": site_defaults(data.get("button_label")),
                "data": {
                    "buttonLabel": get_data_json(data.get("button_label")),
                    "linkType": get_data_json_nested("customLink"),
                    "url": get_data_json("https://www.google.com")
                }
            },
            "imageList": {
                "siteDefaults": site_defaults(images_list),
                "data": converted_images
            }
        }
    
    def convert_product_section(data):
        products_list = data.get("products", [])
        converted_products = []
        for product in products_list:
            converted_product = {
                "productItem": {
                    "siteDefaults": site_defaults(product),
                    "data": {
                        "heading": get_data_json(product.get("name")),
                        "image": get_img_data_json(product.get("image_search_prompt")),
                        "productButton": {
                            "siteDefaults": site_defaults(True),
                            "data": {
                                "linkType": get_data_json_nested("customLink"),
                                "url": get_data_json("https://www.google.com")
                            }
                        },
                        "price": get_data_json(product.get("price"))
                    }
                }
            }
            converted_products.append(converted_product)

        return {
            "heading": get_data_json(data.get("heading")),
            "mainButton": {
                "siteDefaults": site_defaults(data.get("main_button_label")),
                "data": {
                    "buttonLabel": get_data_json(data.get("main_button_label")),
                    "linkType": get_data_json_nested("customLink"),
                    "url": get_data_json("https://www.google.com")
                }
            },
            "productList": {
                "siteDefaults": site_defaults(products_list),
                "data": converted_products
            },
            "productDisplay": {
                "siteDefaults": {"isVisible": True},
                "data": {
                    "showButton": {
                        "siteDefaults": {"isVisible": True},
                        "data": {
                            "buttonLabel": get_data_json(data.get("button_label"))
                        }
                    },
                    "showPrice": {
                        "siteDefaults": {"isVisible": True},
                        "data": {
                            "currency": get_data_json_nested(data.get("currency").lower())
                        }
                    }
                }
            }
        }

    def convert_testimonial_section(data):
        testimonials_list = data.get("testimonials", [])
        converted_testimonials = []
        for testimonial in testimonials_list:
            converted_testimonial = {
                "testimonialsItem": {
                    "siteDefaults": site_defaults(testimonial),
                    "data": {
                        "heading": get_data_json(testimonial.get("quote")),
                        "image": get_img_data_json("Placeholder for testimonial image URL"),
                        "author": get_data_json(testimonial.get("written_by")),
                        "designation": get_data_json(testimonial.get("designation"))
                    }
                }
            }
            converted_testimonials.append(converted_testimonial)

        return {
            "testimonials": {
                "siteDefaults": site_defaults(testimonials_list),
                "data": converted_testimonials
            },
            "heading": get_data_json(data.get("heading"))
        }

    def convert_contact_form(data):
        return {
            "heading": get_data_json(data.get("heading")),
            "contactNo": get_data_json("Placeholder for contact number"),
            "contactEmail": get_data_json("Placeholder for contact email")
        }

    def convert_social_links(data):
        links_list = data.get("links", [])
        converted_links = []
        for link in links_list:
            converted_link = {
                "linkItem": {
                    "siteDefaults": site_defaults(link),
                    "data": {
                        "heading": get_data_json(link.get("type")),
                        "url": get_data_json(link.get("link"))
                    }
                }
            }
            converted_links.append(converted_link)

        return {
            "linksList": {
                "siteDefaults": site_defaults(links_list),
                "data": converted_links
            }
        }




    new_json["blocks"].append(convert_section(key="header", template_key="header", order=1, version=1, data_converter=convert_header))
    new_json["blocks"].append(convert_section(key="intro", template_key="introduction", order=2, version=1, data_converter=convert_intro))
    new_json["blocks"].append(convert_section(key="custom_links", template_key="custom-links", order=3, version=1, data_converter=convert_custom_links))
    new_json["blocks"].append(convert_section(key="services_section", template_key="services", order=4, version=1, data_converter=convert_services_section))
    new_json["blocks"].append(convert_section(key="text", template_key="text", order=2, version=5, data_converter=convert_text))
    new_json["blocks"].append(convert_section(key="gallery_section", template_key="gallery", order=6, version=1, data_converter=convert_gallery_section))
    new_json["blocks"].append(convert_section(key="product_section", template_key="products", order=7, version=1, data_converter=convert_product_section))
    new_json["blocks"].append(convert_section(key="testimonial_section", template_key="testimonials", order=8, version=1, data_converter=convert_testimonial_section))
    new_json["blocks"].append(convert_section(key="contact_form", template_key="contact-form", order=9, version=1, data_converter=convert_contact_form))
    new_json["blocks"].append(convert_section(key="social_links", template_key="social-links", order=10, version=1, data_converter=convert_social_links))

    return new_json

original_data = {
  "header": {
    "title": "Code with Luv",
    "image_search_prompt": "Code with Luv Logo"
  },
  "intro": {
    "heading": "Welcome to Code with Luv",
    "description": "Empower your coding skills with our competitive programming courses.",
    "button_label": "Explore Courses"
  },
  "custom_links": {
    "links": [
      {
        "button_label": "Join Now",
        "button_icon": "icon1"
      },
      {
        "button_label": "Learn More",
        "button_icon": "icon2"
      }
    ]
  },
  "services_section": {
    "heading": "Our Services",
    "button_label": "Book this Course",
    "currency": "USD",
    "services": [
      {
        "name": "Advanced Algorithms",
        "description": "Master advanced algorithms for competitive programming.",
        "price": 99,
        "image_search_prompt": "Advanced Algorithms Course"
      },
      {
        "name": "Dynamic Programming",
        "description": "Learn the art of dynamic programming for competitive coding.",
        "price": 79,
        "image_search_prompt": "Dynamic Programming Course"
      }
    ]
  },
  "text": {
    "heading": "Why Choose Us?",
    "description": "Code with Luv offers top-notch competitive programming courses designed to help you succeed.",
    "button_label": "Learn More"
  },
  "gallery_section": {
    "heading": "Gallery",
    "button_label": "View Gallery",
    "images": [
      {
        "image_description": "Students Studying",
        "image_search_prompt": "Students Studying Competitive Programming"
      },
      {
        "image_description": "Coding Workshop",
        "image_search_prompt": "Coding Workshop for Competitive Programming"
      }
    ]
  },
  "product_section": {
    "heading": "Our Courses",
    "main_button_label": "Explore All Courses",
    "button_label": "Enroll Now",
    "currency": "USD",
    "products": [
      {
        "name": "Advanced Data Structures",
        "price": 129,
        "image_search_prompt": "Advanced Data Structures Course"
      },
      {
        "name": "Graph Theory",
        "price": 89,
        "image_search_prompt": "Graph Theory Course"
      }
    ]
  },
  "testimonial_section": {
    "heading": "Testimonials",
    "testimonials": [
      {
        "quote": "Code with Luv's courses helped me ace coding competitions. Highly recommended!",
        "written_by": "John Doe",
        "designation": "Software Engineer",
        "gender": "male"
      },
      {
        "quote": "I improved my problem-solving skills significantly after taking courses from Code with Luv.",
        "written_by": "Jane Smith",
        "designation": "Student",
        "gender": "female"
      }
    ]
  },
  "contact_form": {
    "heading": "Get in Touch"
  },
  "social_links": {
    "links": [
      {
        "type": "facebook",
        "link": "https://www.facebook.com/codewithluv"
      },
      {
        "type": "twitter",
        "link": "https://www.twitter.com/codewithluv"
      }
    ]
  }
}

converted_data = convert_to_new_format(original_data)

print(converted_data)

