#include <iostream>
#include <mpi.h>
#include <stdio.h>

using namespace std;

int main(int argc, char* argv[])
{
	int errCode;

	if ((errCode = MPI_Init(&argc, &argv)) != 0)
	{
		return errCode;
	}

	int rank, size;
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);

	MPI_Status st;
	int buf = 0;
	if (rank == 0)
	{
		// тут надо for`ом пройтись и передавать куда-то i в сенд
		int buf = 1;
		MPI_Send(&buf, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
	}
	else
	{
		MPI_Recv(&buf, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &st);
		cout << buf << endl;
	}

	MPI_Finalize();
	return 0;
}
