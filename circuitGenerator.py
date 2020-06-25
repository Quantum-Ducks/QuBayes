from qiskit import QuantumCircuit, Aer, execute, IBMQ
from qiskit.providers import JobStatus
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit.providers.aer.noise import NoiseModel
from qiskit.tools.visualization import plot_histogram

graph = {'IR': ([], [.75, .25]),
         'SM': (['IR'], [.3, .8, .7, .2]),
         'OI': ([], [.6, .4]),
         'SP': (['OI', 'SM'], [.9, .5, .4, .2, .1, .5, .6, .8])
        }

def main():
    qbits = num_qbits_needed(graph)
    print("need: " + str(qbits) + " qbits")
    #circuit = QuantumCircuit(1,1)
    #circuit.h(0)
    #circuit.measure(0,0)
    #run_circuit(circuit, "test")

def num_qbits_needed(graph):
    counter = 0
    for state in graph:
        counter += 1
        in_edges = len(graph[state][0])
        if(in_edges != 0):
            counter += in_edges-1
    return counter


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
