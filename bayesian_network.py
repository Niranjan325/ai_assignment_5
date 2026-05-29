from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

model = DiscreteBayesianNetwork([
    ('Rain', 'Traffic')
])

cpd_rain = TabularCPD(
    variable='Rain',
    variable_card=2,
    values=[[0.7],[0.3]]
)

cpd_traffic = TabularCPD(
    variable='Traffic',
    variable_card=2,
    values=[
        [0.9,0.4],
        [0.1,0.6]
    ],
    evidence=['Rain'],
    evidence_card=[2]
)

model.add_cpds(
    cpd_rain,
    cpd_traffic
)

inference = VariableElimination(model)

result = inference.query(
    variables=['Traffic']
)

print(result)
