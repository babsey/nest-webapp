from django.shortcuts import render

import nest

global vm

def setup(request):
    nest.ResetKernel()
    iaf = nest.Create('iaf_neuron')
    ng = nest.Create('noise_generator')
    nest.Connect(ng,iaf)

    vm = nest.Create('voltmeter')

    nest.Connect(vm,iaf)
    return render(request, 'setup.html', {'message':'Success'})


# Create your views here.
def simple_model(request):

    print 'run'
    nest.Simulate(10)
    print 'get'
    Vm_E = nest.GetStatus(vm,'events')[0]

    return render(request, 'simple_model.html', Vm_E)
