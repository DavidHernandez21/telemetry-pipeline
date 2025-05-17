from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem.aggregator import Vector
from diagrams.onprem.database import MongoDB
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ

with Diagram(name="Telemetry collection", show=False, direction="TB"):
    with Cluster("Proxy"):
        ingress = Nginx("ingress")

    with Cluster("Visualization"):
        grafana = Grafana("monitoring")

    with Cluster("Telemetry storage"):
        victoriametrics = Custom("victoriametrics", "./vm.png")
        victoriametrics << Edge(color="firebrick", style="dashed")

        openobserve = Custom("openobserve", "./o2.png")

        telemetry_storage = [
            victoriametrics,
            openobserve,
        ]

    vector = Vector("vector")

    with Cluster("Services Cluster"):
        services = [
            Custom("valkey", "./valkey.png"),
            RabbitMQ("rabbitmq"),
            MongoDB("mongodb"),
        ]

    # vector collects and parse logs and metrics from all services including ingress, grafana, victoriametrics, and openobserve
    vector << Edge(color="blue", style="dotted") << ingress
    vector << Edge(color="blue", style="dotted") << telemetry_storage
    vector << Edge(color="blue", style="dotted") << grafana
    vector << Edge(color="blue", style="dotted") << services

    with Cluster("Vector aggregator"):
        vector_aggregator_primary = Vector("vector")
        (
            vector
            << Edge(color="blue", style="dotted")
            << vector_aggregator_primary
            - Edge(color="brown", style="dotted")
            - Vector("replica")
        )
