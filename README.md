# QuBayes: The Quantum Bayesian Circuit Builder for All

## Exemplified on an original and extremely timely real-world network (for COVID-19)

### Margie Bruff*, Matthew Bryant**, Ella Castelloe*, and Madeline Hunt*
#### *University of North Carolina at Chapel Hill, **North Carolina State University

Project for *Qiskit Community Summer Jam: North Carolina*

### Project Description
The objective of this project is to implement a Bayesian network for COVID-19 in a quantum circuit and use it to calculate probabilities about case and death numbers. We will use data and statistics from the WHO, NIH, and other groups, and we will calculate the probability of a certain country reaching epidemic level case numbers given the implementation of various key policies and restrictions. If we have time we will also add a second stage to our network where we include death rates based on population age and health factors.

If we have time, or to continue work after the campaign, we may also attempt to programmatically determine a quantum circuit for a general Bayesian network, and may attempt to chain the output of one quantum job into the next for a large multi-levelled network.

We will construct our circuit based on the scheme devised by Low et al (2014) and generalized to higher-nodality networks by Borujeni et al (2020). Probability-finding algorithms based on this scheme have been shown analytically to provide a speedup over the best general classical algorithm.

Though the real quantum computer will have significant noise that will affect our results, we expect to get accurate results from the Qiskit Aer simulator. We will compare our simulated results to those from classical networks, and in doing so we will provide an extremely timely and relevant demonstration of the accuracy of this scheme. We will also simplify our main model to one that can be implemented on the real computer, limited in complexity by the number of qubits, and compare results from the simulator with those from the real quantum computer. This will allow us to quantify the effect of current noise levels on this scheme. If we have time, we will also attempt to use Ignus to further study and minimize this noise.

### Usage
The main code is in circuitgenerator.ipynb, this can run inside jupyter-notebooks
and includes functions to create the quantum circuit and to run the
circuit on a simulator or a real quantum computer.

To run our lesser, mallard, or alabio example models, change the input of the graph builder to use the function from network_setup.py corresponding to the model you choose
To make your own model, edit network_setup.py and network_setup.ipynb where indicated at the bottom (import dependencies currently rely on the .py files in all modules other than circuit_generator.ipynb which uses a module import_ipynb that you will need to download, as a result, any changes to depended-on modules will need to be made to both .py and .ipynb versions of the module)

### References
Low, G. H., Yoder, T. J., & Chuang, I. L. (2014). Quantum inference on bayesian networks. Physical Review A, 89 , 062315.

Borujeni, S. E., Nannapaneni, S., Nguyen, N. H., Behrman, E. C., & Steck, J. E. (2020). Quantum circuit representation of Bayesian networks. arXiv pre-print: https://arxiv.org/pdf/2004.14803.pdf
