from string import Template

A = ("C        -3.6180905689    1.3768035675   -0.0207958979\n"
     "O        -4.7356838533    1.5255563000    0.1150239130")
B = ("O        -7.9563726699    1.4854060709    0.1167920007\n"
     "H        -6.9923165534    1.4211335985    0.1774706091\n"
     "H        -8.1058463545    2.4422204631    0.1115993752")
pc = ("-7.9563726699    1.4854060709    0.1167920007    -0.8\n"
      "-6.9923165534    1.4211335985    0.1774706091     0.4\n"
      "-8.1058463545    2.4422204631    0.1115993752     0.4")

defaults = {
    "basis"            : "cc-pVDZ",
    "charge"           : 0,
    "charge_tot"       : 0,
    "charge_a"         : 0,
    "charge_b"         : 0,
    "expansion"        : "SE",
    "frag_a"           : A,
    "frag_b"           : B,
    "memory"           : 15000,
    "method"           : "HF",
    "molden"           : "false",
    "multiplicity"     : 1,
    "multiplicity_tot" : 1,
    "multiplicity_a"   : 1,
    "multiplicity_b"   : 1,
    "nstates"          : 0,
    "t_func"           : "TF",
    "xc_func"          : "PBE",
    "x_func"           : "Slater",
    "c_func"           : "VWN5",
    "xc_func_b"        : "PBE",
    "xyz"              : A,
    "print_orbitals"   : 15,
    "point_charges"    : pc,
    "aux_memory"       : 20000,
    "comment"          : "generated from CCJob.Templates",
    "opt_conv_energy"  : 150,
    "opt_conv_displace": 1200,
    "opt_conv_grad"    : 300,
    "opt_max_cycles"   : 50,
    "opt_dmax"         : 300
            }

ADC = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = $nstates
basis = $basis
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
molden_format = $molden
state_analysis = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge $multiplicity
$xyz
$$end""")

MP2_exportDens = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = 0
basis $basis
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
state_analysis = true
print_orbitals = $print_orbitals
gen_scfman = false
fde_only_export_B = true
$$end

$$molecule
$charge $multiplicity
$xyz                     
$$end""")

MP2_prepolExportDens = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = 0
basis $basis
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
state_analysis = true
print_orbitals = $print_orbitals
gen_scfman = false
scf_final_print = 1
fde_only_export_B = true
$$end

$$molecule
$charge $multiplicity
$xyz                     
$$end

$$external_charges
$point_charges
$$end

@@@

$$molecule
read
$$end

$$rem
sym_ignore = true
method = hf
gen_scfman = false
basis = $basis
mem_static = 1024
mem_total = $aux_memory
scf_guess = read
max_scf_cycles = 0
scf_final_print = 1
$$end
""")

ADCinHF = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = $nstates
basis = $basis
fde true
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
!molden_format = true
state_analysis = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
T_Func $t_func
XC_Func $xc_func
expansion $expansion
rhoB_method HF
rhoA_method mp
PrintLevel 3
debug true
$$end""")

ADCinHF_X_C = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = $nstates
basis = $basis
fde true
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
!molden_format = true
state_analysis = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
T_Func $t_func
X_Func $x_func
C_Func $c_func
expansion $expansion
rhoB_method HF
rhoA_method mp
PrintLevel 3
debug true
$$end""")

ADCinDFT = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = $nstates
basis  = $basis
fde = true
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
!molden_format = true
state_analysis = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
T_Func $t_func
XC_Func $xc_func
expansion super
rhoB_method DFT
rhoA_method mp
XC_Func_B $xc_func_b
PrintLevel 3
debug true
$$end""")

ADCin_MP2 = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = 0
basis = $basis
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
state_analysis = true
print_orbitals = $print_orbitals
gen_scfman = false
fde_only_export_B = true
$$end

$$molecule
$charge_b $multiplicity_b
$frag_b_bse                    
$$end

@@@

$$rem
sym_ignore = true
method = adc(2)
ee_states = $nstates
basis  = $basis
fde = true
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
!molden_format = true
state_analysis = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
import_rho_B true
rhoA_method mp
T_Func $t_func
XC_Func $xc_func
expansion $expansion
PrintLevel 3
debug true
$$end""")

ADCin_MP2_X_C = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = 0
basis = $basis
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
state_analysis = true
print_orbitals = $print_orbitals
gen_scfman = false
fde_only_export_B = true
$$end

$$molecule
$charge_b $multiplicity_b
$frag_b_bse                    
$$end

@@@

$$rem
sym_ignore = true
method = adc(2)
ee_states = $nstates
basis  = $basis
fde = true
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
!molden_format = true
state_analysis = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
import_rho_B true
rhoA_method mp
T_Func $t_func
X_Func $x_func
C_Func $c_func
expansion $expansion
PrintLevel 3
debug true
$$end""")

ADCin_impB = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = $nstates
basis  = $basis
fde = true
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
!molden_format = true
state_analysis = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
import_rho_B true
T_Func $t_func
XC_Func $xc_func
expansion $expansion
rhoA_method mp
PrintLevel 3
debug true
$$end""")

ADCin_impB_X_C = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = $nstates
basis  = $basis
fde = true
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
!molden_format = true
state_analysis = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
import_rho_B true
rhoA_method mp
T_Func $t_func
X_Func $x_func
C_Func $c_func
expansion $expansion
PrintLevel 3
debug true
$$end""")


ADCin_impAB = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = $nstates
basis  = $basis
fde = true
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
!molden_format = true
state_analysis = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
import_rho_A true
import_rho_B true
T_Func $t_func
XC_Func $xc_func
expansion $expansion
PrintLevel 3
debug true
$$end""")

ADCin_impAB_X_C = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = adc(2)
ee_states = $nstates
basis  = $basis
fde = true
mem_static = 1024
mem_total = $memory
adc_davidson_maxiter = 900
adc_davidson_conv = 6
adc_print = 3
adc_prop_es = true
!molden_format = true
state_analysis = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
import_rho_A true
import_rho_B true
T_Func $t_func
X_Func $x_func
C_Func $c_func
expansion $expansion
PrintLevel 3
debug true
$$end""")

HFinHF = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = hf
gen_scfman = false
basis = $basis
fde = true
mem_static = 1024
mem_total = $memory
!molden_format = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
T_Func $t_func
XC_Func $xc_func
expansion $expansion
rhoB_method HF
PrintLevel 3
debug true
$$end""")

HFinHF_X_C = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = hf
gen_scfman = false
basis = $basis
fde = true
mem_static = 1024
mem_total = $memory
!molden_format = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
T_Func $t_func
X_Func $x_func
C_Func $c_func
expansion $expansion
rhoB_method HF
PrintLevel 3
debug true
$$end""")

HFinHF_impA = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = hf
gen_scfman = false
basis = $basis
fde true
mem_static = 1024
mem_total = $memory
!molden_format = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
import_rho_A true
T_Func $t_func
XC_Func $xc_func
expansion $expansion
rhoB_method HF
PrintLevel 3
debug true
$$end""")

HFinHF_impB = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = hf
gen_scfman = false
basis = $basis
fde = true
mem_static = 1024
mem_total = $memory
!molden_format = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
import_rho_B true
T_Func $t_func
XC_Func $xc_func
expansion $expansion
PrintLevel 3
debug true
$$end""")

HFinHF_impB_X_C = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = hf
gen_scfman = false
basis = $basis
fde = true
mem_static = 1024
mem_total = $memory
!molden_format = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
import_rho_B true
T_Func $t_func
X_Func $x_func
C_Func $c_func
expansion $expansion
PrintLevel 3
debug true
$$end""")

HFinHF_impAB = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = hf
gen_scfman = false
basis = $basis
fde = true
mem_static = 1024
mem_total = $memory
!molden_format = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
import_rho_A true
import_rho_B true
T_Func $t_func
XC_Func $xc_func
expansion $expansion
PrintLevel 3
debug true
$$end""")

HFinHF_impAB_X_C = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = hf
gen_scfman = false
basis = $basis
fde = true
mem_static = 1024
mem_total = $memory
!molden_format = true
print_orbitals = $print_orbitals
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end

$$fde
import_rho_A true
import_rho_B true
T_Func $t_func
X_Func $x_func
C_Func $c_func
expansion $expansion
PrintLevel 3
debug true
$$end""")

HF_extend = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
method = hf
basis = $basis
mem_static = 1024
mem_total = $memory
molden_format = true
print_orbitals = $print_orbitals
scf_final_print = 1
scf_convergence = 6
iprint = 200
$$end

$$molecule
$charge $multiplicity
$xyz
$$end""")

HF_prepolExportDens = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
gen_scfman = false
method = hf
basis = $basis
mem_static = 1024
mem_total = $memory
scf_final_print = 1
fde_only_export_B = true
$$end

$$molecule
$charge $multiplicity
$xyz
$$end

$$external_charges
$point_charges
$$end

@@@

$$molecule
read
$$end

$$rem
sym_ignore = true
method = hf
gen_scfman = false
basis = $basis
mem_static = 1024
mem_total = $aux_memory
scf_guess = read
max_scf_cycles = 0
scf_final_print = 1
$$end""")

HF_chelpg = Template("""$$comment
$comment
$$end

$$rem
sym_ignore = true
gen_scfman = false
method = hf
basis = $basis
mem_static = 1024
mem_total = $memory
chelpg = true
chelpg_head = 30
chelpg_dx = 6
$$end

$$molecule
$charge $multiplicity
$xyz
$$end""")

SAPT0_Psi4 = Template("""
import psi4

# set output format
# second argument --> bool append
psi4.core.set_output_file($output, False)

# set memory and CPUs
psi4.set_memory("$memory GB")
psi4.set_num_threads($cpus)

mol = psi4.geometry($molecule)

opt = {"scf_type" : "df",
       "freeze_core" : "true"}
psi4.set_options(opt)
psi4.energy("sapt0/cc-pVDZ", molecule=mol)

print_out("Yay, I finished!")
""")

SAPT0_std = Template("""
import psi4

# set output format
# second argument --> bool append
psi4.core.set_output_file("$output", False)

# set memory and CPUs
psi4.set_memory("$memory GB")
psi4.set_num_threads($cpus)

mol = psi4.geometry('''
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
units angstrom
''')

opt = {"scf_type" : "df",
       "freeze_core" : "true"}
psi4.set_options(opt)
psi4.energy("sapt0/$basis", molecule=mol)

print_out("Yay, I finished!")
""")

ALMO2_HF = Template("""$$comment
$comment
$$end

$$rem
jobtype = eda
eda2 = 1 !nDQ
method = hf
basis = $basis
symmetry = false
sym_ignore = true
mem_static = 1024
mem_total = $memory
thresh = 14
scf_convergence = 8
!frgm_method = stoll
eda_bsse = true
n_frozen_core = 0
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end
""")

ALMO2_MP2 = Template("""$$comment
$comment
$$end

$$rem
jobtype = eda
eda2 = 1 !nDQ
exchange = hf
correlation = rimp2
basis = $basis
aux_basis = $aux_basis
symmetry = false
mem_static = 1024
mem_total = $memory
thresh = 14
scf_convergence = 8
frgm_method = stoll
eda_bsse = true
n_frozen_core = 0
$$end

$$molecule
$charge_tot $multiplicity_tot
--
$charge_a $multiplicity_a
$frag_a
--
$charge_b $multiplicity_b
$frag_b
$$end
""")

opt_freq_std = Template("""$$comment
$comment
$$end

$$rem
jobtype = opt
method = $method
basis  = $basis
thresh = 14
use_libqints = 1
mem_static = 1024
mem_total = $memory
geom_opt_tol_energy = $opt_conv_energy !default: 150
geom_opt_tol_displacement = $opt_conv_displace !default: 1200
geom_opt_tol_gradient = $opt_conv_grad !default: 300
geom_opt_max_cycles = $opt_max_cycles !default: 50
geom_opt_dmax = $opt_dmax !default: 300
$$end

$$molecule
$charge $multiplicity
$xyz
$$end

@@@

$$rem
jobtype = freq
method = $method
basis = $basis
thresh = 14
use_libqints = 1
mem_static = 1024
mem_total = $memory
$$end

$$molecule
  read
$$end
""")

