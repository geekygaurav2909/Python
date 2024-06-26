import requests as reqs
from datetime import datetime

USERNAME = "YOUR USER NAME"
TOKEN = "Token ID"
GRAPH_ID = "Your graph id"

pixela_endpoint = "https://pixe.la/v1/users"
user_parameter = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# user_creation = reqs.post(url=pixela_endpoint, json=user_parameter)
# print(user_creation.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_parameter = {
    "id": GRAPH_ID,
    "name": "Coding Graph",
    "unit": "hour",
    "type": "float",
    "color": "ajisai"
}

graph_headers = {
    "X-USER-TOKEN": TOKEN
}

# graph_resp = reqs.post(url=graph_endpoint, json=graph_parameter, headers=graph_headers)
# print(graph_resp.text)

post_graph_value = f"{graph_endpoint}/{GRAPH_ID}"

date = datetime.now()
date_format = date.strftime("%Y%m%d")

value_param = {
    "date": date_format,
    "quantity": input("How many hours did you code today?: ")
}

value_resp = reqs.post(url=post_graph_value, json=value_param, headers=graph_headers)
print(value_resp.text)

# Updating the graph data from UTC time zone to IST

# timezone_para = {
#     "timezone": "Asia/Calcutta"
# }
#
# updatezone_resp = reqs.put(url=post_graph_value, json=timezone_para, headers=graph_headers)
# print(updatezone_resp.text)

# Updating a pixel

update_url = f"{post_graph_value}/{date_format}"

qty_para = {
    "quantity": "2.5"
}

# response = reqs.put(url=update_url, json=qty_para, headers=graph_headers)
# print(response.text)

# Deleting a pixel

# response = reqs.delete(url=update_url, headers=graph_headers)
# print(response.text)
