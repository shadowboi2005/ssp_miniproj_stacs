#include <stdio.h>
#include <math.h>
#include <stdbool.h>


struct star {
    double x;
    double y;
    int B;
};

bool chkdist(struct star star1, struct star star2 , int aroi){
    double val = pow((star1.x - star2.x) , 2) + pow((star1.y - star2.y),2) ;
    if (val < pow(aroi - 2 , 2))
    {
        return 1;
    }
    else{
        return 0;
    }
     
}


void centroid_with_just_intensity(int** intensityarr,int m, int n,int aroi,struct star* possible_stars){

}



int main(){
    FILE * fileptr;
    fileptr = fopen("fname" , "r");
    int height;
    int width;

    
    fscanf(fileptr, "%d," ,&height);
    fscanf(fileptr, "%d" , &width);
    int numarr[height][width];
    
    for(int i=0;i<height;i++){
        for(int j = 0; j<width;j++){
            fscanf(fileptr,"%d," , &numarr[i][j]);
        }
    }
    printf("read!");
    /*

    
    for(int i=0;i<height;i++){
        for(int j = 0; j<width;j++){
            printf("(%d ,%d) element of the array is  : %d \n",i+1,j+1,numarr[i][j]);
        }
    }
    */
}