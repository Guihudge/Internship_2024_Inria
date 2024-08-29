#include <iostream>
#include <cstdlib>
#include <chrono>
#include <omp.h>
// #define MAPHYSPP_HEADER_ONLY
#include <maphys.hpp>
#include <mkl_service.h>

using namespace std;

template <typename T>
void printMat(T &mat)
{
    for (auto &row : mat)
    {
        for (auto &col : row)
        {
            cout << '\t' << col;
        }
        cout << '\n';
    }
}

int usage(char *cmd)
{
    cerr << cmd << " m n p BLOCK_SIZE"
         << "\n"
         << "Reminder: \n"
         << "  A(m, n) \n  B(n, p)\n";
    return EXIT_FAILURE;
}

int main(int argc, char **argv)
{
    {
        using namespace maphys;
        // Init des variables
        int MAX = 10;
        int BLOCK_SIZE, m, n, p;

        if (argc == 5)
        {
            n = strtol(argv[1], NULL, 10);
            m = strtol(argv[2], NULL, 10);
            p = strtol(argv[3], NULL, 10);
            BLOCK_SIZE = strtol(argv[4], NULL, 10);
        }
        else
        {
            return usage(argv[0]);
        }

        using namespace std::chrono;
        auto t1 = high_resolution_clock::now();

        if (m % BLOCK_SIZE != 0 || p % BLOCK_SIZE != 0)
        {
            cout << "Invalid BLOCK_SIZE\n";
            return EXIT_FAILURE;
        }

        cerr << "Info: using BLOCK_SIZE=" << BLOCK_SIZE << "\n";

        DenseMatrix<double> A(m, n);
        DenseMatrix<double> B(n, p);
        DenseMatrix<double> C(m, p);

        using namespace maphys;
        // remplissage des matrice avec des valeurs aléatoires
        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                A(i, j) = rand() % MAX;
            }
        }

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < p; j++)
            {
                B(i, j) = rand() % MAX;
            }
        }

        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < p; j++)
            {
                C(i, j) = 0;
            }
        }

        DenseMatrix<double> verifC = A * B;

        auto t2 = high_resolution_clock::now();
        int omp_nbthread = -1;
        int mkl_nbthread = -1;

        omp_nbthread = omp_get_num_threads();
        mkl_nbthread = mkl_get_max_threads();
        cerr << "befor omp: mkl threads=" << mkl_nbthread << "omp_thread=" << omp_nbthread << "\n";

        // Calcule
#pragma omp parallel master
        {
            omp_nbthread = omp_get_num_threads();
            mkl_nbthread = mkl_get_max_threads();
            cerr << "omp init: mkl threads=" << mkl_nbthread << " omp_thread=" << omp_nbthread << "\n";
            if (omp_nbthread == 1) // Si on est sur un coeur on utilise directement l'opération de compose
            {
                t2 = high_resolution_clock::now();
                cerr << "Sequentiel\n";
                mkl_set_num_threads(4);
                C = A * B;
            }
            else
            {
                cerr << "Parallèle\n";
                
#pragma omp taskloop collapse(2) shared(C)
                for (int i = 0; i < m; i += BLOCK_SIZE)
                {
                    for (int j = 0; j < p; j += BLOCK_SIZE)
                    {
                        //mkl_set_num_threads(2);
                        DenseMatrix<double> tmpA = A.get_block_view(i, 0, BLOCK_SIZE, n);
                        DenseMatrix<double> tmpB = B.get_block_view(0, j, n, BLOCK_SIZE);
                        // DenseMatrix<double> tmpC(BLOCK_SIZE, BLOCK_SIZE);
                        // tmpC = (tmpA * tmpB);
                        // tmpC.display("tmp:");
                        C.get_block_view(i, j, BLOCK_SIZE, BLOCK_SIZE) = tmpA * tmpB;
                    }
                }
            }
        }

        auto t3 = high_resolution_clock::now();

        // On vérifie le résultat
        
        // std::cout<<(verifC - C).norm();
        if ((verifC - C).norm() > 10e-15)
        {
            cout << "Matrice différante\n";
            return EXIT_FAILURE;
        }

        // Affichage des stats
        auto init = duration_cast<milliseconds>(t2 - t1);
        auto compute = duration_cast<milliseconds>(t3 - t2);

        cout << "{\"init\":" << init.count() << ",\"compute\":" << compute.count() << ",\"nbThread\":" << omp_nbthread << ",\"blockSize\":" << BLOCK_SIZE << "}\n";
    }
}

// Vieux code
/*
#pragma omp parallel master
{
nbthread = omp_get_num_threads();
#pragma omp taskloop grainsize(20)
for (int i = 0; i < m; i++)
{

    //cout << omp_get_thread_num() << "\n";
    for (int j = 0; j < p; j++)
    {
        for (int k = 0; k < n; k++)
        {
            matC[i][j] += matA[i][k] * matB[k][j];
        }
    }
}
#pragma omp taskwait
}*/
// cout << "\tInit:\t" << init.count() << "ms\n";
// cout << "\tCompute:\t" << compute.count() << "ms\n";

// C.display("Result:");