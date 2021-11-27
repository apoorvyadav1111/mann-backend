import graphene

def global_id_to_primary_id(encoded_id):
	return graphene.relay.Node.from_global_id(encoded_id)