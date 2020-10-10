webapps = [{"id": 1, "link_name": "Kakatoo", "link_url": "https://mango.com"},
           {"id": 2, "link_name": "Mango", "link_url": "https://mango.com"},
           {"id": 3, "link_name": "Hase", "link_url": "https://mango.com"},
           {"id": 4, "link_name": "Kolibri", "link_url": "https://mango.com"},
           {"id": 5, "link_name": "Apfel", "link_url": "https://mango.com"},
           {"id": 6, "link_name": "Kirsche", "link_url": "https://mango.com"},
           {"id": 7, "link_name": "Panda", "link_url": "https://mango.com"},
           {"id": 8, "link_name": "Schmetterling", "link_url": "https://mango.com"}]

users = [{"id": 1,
          "firstname": "Mandarin",
          "name": "Orange",
          "username": "s77518",
          "primary_email": 'bird@kakadu.com',
          "all_emails": ['bird@kakadu.com', 'kakadu@kamel.de', 's87r2390@uni.de', 'dasdas@university.de'],
          "admin": True,
          "webapps": webapps,
          "user_groups": ['Kubernetes users'],
          "k8s_serviceaccount": 'default',
          "k8s_namespace": 'default',
          "k8s_token": 'default',
          "k8s_apiserver": 'default',
          "k8s_clustername": 'default',
          "cluster_access": 'approved'
          }
         ]


cluster_info = {"portal_user_count": "120", "portal_version": "v.0.3.16", "k8s_version": "v1.15.4",
                "k8s_node_count": "24", "k8s_cpu_count": "1536", "k8s_mem_sum": "12543.876796Gi",
                "k8s_pod_count": 723, "k8s_volume_count": 227, "k8s_apiserver_url": "https://10.96.0.1:443",
                "k8s_cluster_name": "clustername"}

groups = [{"id": 1, "group_name": "Kubernetes User"}, {"id": 2, "group_name": "Datexis SHK"}]
