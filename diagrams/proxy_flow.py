from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ

with Diagram(name="Proxy flow", show=False):
    with Cluster("Proxy"):
        ingress = Nginx("ingress")

    (
        ingress
        >> Edge(
            color="darkgreen",
            style="normal",
            label="/victoriametrics",
            fontsize="18",
        )
        >> Custom("victoriametrics", "./vm.png")
    )
    (
        ingress
        >> Edge(color="darkblue", style="normal", label="/openobserve", fontsize="18")
        >> Custom("openobserve", "./o2.png")
    )
    (
        ingress
        >> Edge(color="darkbrown", style="normal", label="/grafana", fontsize="18")
        >> Grafana("monitoring")
    )
    (
        ingress
        >> Edge(color="darkred", style="normal", label="/rabbitmq", fontsize="18")
        >> RabbitMQ("rabbitmq management")
    )
