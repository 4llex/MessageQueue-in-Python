// Your First C++ Program
// Compiling C program: $ sudo gcc –o first first.c
//                          or
//                  	$ sudo gcc first.c
// ----------------------------------------------------
// Compiling C++ program: $ sudo g++ hello.cpp
// 				 or
// 			  $ sudo g++ -o hello hello.cpp


#include <iostream>
#include <pmt/api.h>
#include <pmt/pmt_sugar.h>
#include <pmt/pmt.h>

#include <stdlib.h>
#include <math.h>
#include <complex.h>
#include <string.h>


int main() {
    std::cout << "Hello World! \n";

    pmt::pmt_t P = pmt::from_long(23);
    std::cout << P << std::endl;
    pmt::pmt_t P2 = pmt::from_complex(0, 1); // Alternatively: pmt::from_complex(0, 1)
    std::cout << P2 << std::endl;
    std::cout << pmt::is_complex(P2) << std::endl;

    return 0;
}
