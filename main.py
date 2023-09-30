git remote set-url origin https://github.com/CSE6805-EA-April23/nsga2_recommender.git#NSGA 2 version 1
'''
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

# Define a multi-objective optimization problem (e.g., ZDT1)
problem = get_problem("zdt1")

# Create an instance of the NSGA-II algorithm
algorithm = NSGA2(pop_size=100)

# Perform the optimization
res = minimize(problem,
               algorithm,
               termination=('n_gen', 100),
               seed=1,
               save_history=True,
               verbose=True)

# Access and print the optimal solutions found
print("Best solutions found:")
for solution in res.pop:
    print(f"Objective values: {solution.F}")
    print(f"Decision variables: {solution.X}")
    print()

# Visualize the Pareto front
plot = Scatter()
plot.add(res.F, color="red")
plot.show()
'''

#NSGA 2 version 2;Moreover, we can customize NSGA-II to solve a problem with binary decision variables, for example, ZDT5.
'''
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

problem = get_problem("zdt5")

algorithm = NSGA2(pop_size=100,
                  sampling=BinaryRandomSampling(),
                  crossover=TwoPointCrossover(),
                  mutation=BitflipMutation(),
                  eliminate_duplicates=True)

res = minimize(problem,
               algorithm,
               ('n_gen', 500),
               seed=1,
               verbose=False)

Scatter().add(res.F).show()
'''

# Import necessary modules from Pymoo
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

# Define a multi-objective optimization problem (e.g., ZDT1)
problem = get_problem("zdt1")

# Create an instance of the NSGA-II algorithm
algorithm = NSGA2(pop_size=100)

# Perform the optimization
res = minimize(problem,
               algorithm,
               termination=('n_gen', 100),
               seed=1,
               save_history=True,
               verbose=True)

# Access and print the optimal solutions found
print("Best solutions found:")
for solution in res.pop:
    print(f"Objective values: {solution.F}")
    print(f"Decision variables: {solution.X}")
    print()

# Visualize the Pareto front
plot = Scatter()
plot.add(res.F, color="red")
plot.show()

'''from pymoo.optimize import minimize
from pymoo.factory import get_problem
from pymoo.visualization.scatter import Scatter



from pymoo.model.problem import Problem
import numpy as np
import matplotlib.pyplot as plt
from deap import benchmark

class ProblemWrapper(Problem):
    def _evaluate(self,designs,out,*args,**kwargs):
        res=[]
        for design in designs:
            res.append(benchmarks.kursawe(design))
        out['F']=np.array(res)
problem = ProblemWrapper(n_var=2,n_obj=2,xl=[-5.,-5.],xu=[5.,5.])
from pymoo.algorithms.nsga2 import NSGA2
algorithm=NSGA2[pop_size=100]
stop_criteria=('n_gen',100)
results=minimize(
    problem=problem,
    algorithm=algorithm,
    termination=stop_criteria)
import plotly.graph_objects as go
fig = go.figure(data=go.Scatter(x = res_data[0],y = res_data[1], model='makers'))
fig.show()'''