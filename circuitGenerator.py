from qiskit import QuantumCircuit, Aer, execute, IBMQ
from qiskit.providers import JobStatus
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit.providers.aer.noise import NoiseModel
from qiskit.tools.visualization import plot_histogram
from math import atan2, sqrt

basic_graph = { 'A': ([], [.2, .8]),
                'B': ([], [.3, .7]),
                'C': (['A','B'], [.15, .85, .3, .7, .4, .6, .1, .9])
              }
#ir = q4, oi = q3, sm = q2, sp = q0
# why does the paper do this
# XXX figure 11 is bad, too many magic numbers
oil_graph = {'IR': ([], [.75, .25]), # From 2004.14803, Fig 10
         'SM': (['IR'], [.3, .7, .8, .2]), #P(0|!A), P(1|!A), P(0|A), P(1|A)
         'OI': ([], [.6, .4]),
         'SP': (['OI', 'SM'], [.9, .1, .5, .5, .4, .6, .2, .8])
        }

def main():
    circuit = create_circuit(basic_graph)
    run_circuit(circuit, "test")

# TODO auto generate the circuit
def create_circuit(graph):
    (qbits, cbits) = num_qbits_needed(graph)
    qc = QuantumCircuit(qbits, cbits)
    bit_assignment = {}
    ancillabits = []
    next_free_qbit = 0
    #Loop and find the parentless nodes, assign their rotations first
    for node in graph:
        if len(graph[node][0])==0:
            probs = graph[node][1]
            qc.ry(angle_from_probability(probs[1],probs[0]), next_free_qbit)
            bit_assignment[node] = next_free_qbit # keep track of what node is what qbit
            next_free_qbit += 1
    qc.barrier()

    #Loop and find each node that has all its parents complete and add it
    #TODO a topological sort first would save this unnessacary looping
    #XXX bad code, maybe the worst
    while True: # Loop until no states are added
        found_new = False
        for node in graph:
            if node not in bit_assignment:
                for parent in node[0]:  # get parents
                    if parent not in bit_assignment:
                        continue  # one of the parents needs to be processed first
                # Found a node we are ready to process
                found_new = True
                # TODO handle multi-bit states
                bit_assignment[node] = next_free_qbit # give it a qbit
                next_free_qbit += 1
                # FIXME hardcoded 1/2 parent, will generalize later
                if len(graph[node]) == 1:
                    print("1 parent not implemented") 
                    raise NotImplementedError
                if len(graph[node]) == 2:
                    # TODO this is gross
                    print(bit_assignment)
                    if(len(ancillabits) < 1): # need one more ancilla bit
                        ancillabits += [next_free_qbit]
                        next_free_qbit+=1
                    parent1 = bit_assignment[graph[node][0][0]]
                    parent2 = bit_assignment[graph[node][0][1]]
                    target = bit_assignment[node]
                    # |00>
                    qc.x(parent1)
                    qc.x(parent2)
                    # XXX ahhh this is horrible but will work for a demo
                    angle = angle_from_probability(graph[node][1][1], graph[node][1][0])
                    add_ccy(qc, [parent1,parent2,target], angle, ancillabits[0])
                    qc.x(parent1)
                    qc.x(parent2)
                    # |01>
                    qc.x(parent1)
                    angle = angle_from_probability(graph[node][1][3], graph[node][1][2])
                    add_ccy(qc, [parent1,parent2,target], angle, ancillabits[0])
                    qc.x(parent1)
                    # |10>
                    qc.x(parent2)
                    angle = angle_from_probability(graph[node][1][5], graph[node][1][4])
                    add_ccy(qc, [parent1,parent2,target], angle, ancillabits[0])
                    qc.x(parent2)
                    # |11>
                    angle = angle_from_probability(graph[node][1][7], graph[node][1][6])
                    add_ccy(qc, [parent1,parent2,target], angle, ancillabits[0])
                break  # start looping again, painfully inefficient
        if not found_new:
            break # Completed a full loop over the nodes and all were added, done

    c_counter = 0
    for bit in bit_assignment:
        qc.measure(bit_assignment[bit], c_counter)
        c_counter += 1
    return qc

# TODO Code section 3.2
# XXX Can we generalize this to C^nY gates
# ex: add_ccy(qc, [0,1,2], math.pi/3, 3)
def add_ccy(circuit, qbits, angle, ancillabit):
    # XXX Should we use this link instead of this function:
    # https://qiskit.org/documentation/tutorials/circuits_advanced/1_advanced_circuits.html
    circuit.barrier() # for visualization
    circuit.ccx(qbits[0], qbits[1], ancillabit)
    circuit.ry(angle/2,qbits[2])
    circuit.cx(ancillabit, qbits[2])
    circuit.ry(-angle/2, qbits[2] )
    circuit.cx(ancillabit, qbits[2])
    circuit.ccx(qbits[0], qbits[1], ancillabit)
    circuit.barrier() # for visualization

def num_qbits_needed(graph):
    max_edges = -1 
    for state in graph:
        in_edges = len(graph[state][0]) # aka num of parents
        if in_edges > max_edges:
            max_edges = in_edges
    
    qbits = len(graph) + max_edges - 1 # equation (15)
    cbits = len(graph) # number of measurements
    return (qbits, cbits)

#TODO assertAlmostEqual(angle_from_probability(.8,.2), 2.2143)
def angle_from_probability(p1, p0):
    # From 2004.14803 equation 20
    return 2 * atan2(sqrt(p1), sqrt(p0))

def run_circuit(circuit, output_file='results', draw_circuit=True, use_sim=True, use_noise=False, use_qcomp=False):
    if draw_circuit:
        print(circuit.draw())

    if use_noise or use_qcomp:
        IBMQ.load_account()
        provider = IBMQ.get_provider('ibm-q')
        qcomp = provider.get_backend('ibmq_16_melbourne')

    if use_sim:
        simulator = Aer.get_backend('qasm_simulator')
        if use_noise:
            noise_model = NoiseModel.from_backend(qcomp)
            basis_gates = noise_model.basis_gates
            coupling_map = qcomp.configuration().coupling_map
            job = execute(circuit, backend=simulator, coupling_map=coupling_map, noise_model=noise_model, basis_gates=basis_gates, shots=1024)
        else:
            job = execute(circuit, backend=simulator)
        print(job.result().get_counts())
        plot_histogram(job.result().get_counts()).savefig(output_file+'-sim.png')


    if use_qcomp:
        job = execute(circuit, backend=qcomp, shots=1024)
        job_monitor(job)
        if(job.status() == JobStatus.ERROR):
            print("Error: Check with IBMQ")
        print(job.result().get_counts())
        plot_histogram(job.result().get_counts()).savefig(output_file+'-qcomp.png')

if __name__ == "__main__":
    main()
