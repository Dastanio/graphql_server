from ssl import SSLContext
from ssl import CERT_REQUIRED
from ssl import PROTOCOL_TLSv1_2
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra import ConsistencyLevel
from cassandra.query import dict_factory


def create_cassandra_connection(db_username, db_password, db_host, db_port, db_local_dc):
    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    ssl_context.load_verify_locations('layers/AmazonRootCA1.pem')
    ssl_context.verify_mode = CERT_REQUIRED
    auth_provider = PlainTextAuthProvider(username=db_username, password=db_password)
    default_profile = ExecutionProfile(
        load_balancing_policy=DCAwareRoundRobinPolicy(local_dc=db_local_dc),
        consistency_level=ConsistencyLevel.LOCAL_QUORUM,
        request_timeout=60,
        row_factory=dict_factory
    )
    cluster = Cluster(
        db_host,
        ssl_context=ssl_context,
        auth_provider=auth_provider,
        port=db_port,
        protocol_version=4,
        connect_timeout=60,
        idle_heartbeat_interval=0,
        execution_profiles={EXEC_PROFILE_DEFAULT: default_profile}
    )
    connection = cluster.connect()
    return connection
