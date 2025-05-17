from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem.aggregator import Vector
from diagrams.onprem.database import MongoDB
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ

with Diagram(name="Pipeline flow", show=False):
    with Cluster("Proxy"):
        ingress = Nginx("ingress")

    with Cluster("Visualization"):
        grafana = Grafana("monitoring")

    with Cluster("Telemetry storage"):
        victoriametrics = Custom("victoriametrics", "./vm.png")
        victoriametrics << Edge(color="firebrick", style="dashed") << grafana

        openobserve = Custom("openobserve", "./o2.png")

        (
            openobserve
            << Edge(color="firebrick", style="dotted", label="optional")
            << grafana
        )

    vector = Vector("vector")

    with Cluster("Services Cluster"):
        services = [
            Custom("valkey", "./valkey.png"),
            RabbitMQ("rabbitmq"),
            MongoDB("mongodb"),
        ]

    services >> Edge(color="firebrick", style="dashed") >> vector
    vector >> Edge(color="firebrick", style="bold", label="push") >> ingress

    with Cluster("Vector aggregator"):
        vector_aggregator_primary = Vector("vector")
        vector_aggregator_replica = Vector("replica")

        vector_aggregator_cluster = [
            vector_aggregator_primary,
            vector_aggregator_replica,
        ]

    (
        vector_aggregator_cluster
        >> Edge(color="darkgreen", style="dashed")
        >> victoriametrics
    )
    vector_aggregator_cluster >> Edge(color="darkblue", style="dashed") >> openobserve
    (
        ingress
        >> Edge(color="darkbrown", style="normal", label="load balance")
        >> vector_aggregator_primary
    )
    (
        ingress
        >> Edge(color="darkbrown", style="dotted", label="load balance")
        >> vector_aggregator_replica
    )
