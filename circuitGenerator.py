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
    #XXX how to keep track as to what bits are used and what for
    next_free_qbit = 0
    #Loop and find the parentless nodes, assign their rotations first
    for node in graph:
        if len(graph[node][0])==0:
            #Gross graph work
            probs = graph[node][1]
            print(probs)
            qc.ry(angle_from_probability(probs[1],probs[0]), next_free_qbit)
            next_free_qbit += 1
    qc.barrier()
    return qc

# TODO Code section 3.2
# XXX Can we generalize this to C^nY gates
def add_ccy(circuit, qbits, ancillabits):
    pass

#XXX Gross
def num_qbits_needed(graph):
    qbits = 0
    cbits = 0
    for state in graph:
        qbits += 1
        cbits += 1
        in_edges = len(graph[state][0])
        if in_edges != 0: # count ancilla qbits
            qbits += in_edges-1
    return (qbits, cbits)

#TODO assertAlmostEqual(angle_from_probability(.8,.2), 2.2143)
def angle_from_probability(p1, p0):
    #XXX atan2 here?
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
