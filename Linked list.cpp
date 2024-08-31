#include<iostream>
using namespace std;

class node{

    public :
    int data;
    node* next;

    node(int value){
        data=value;
        next=NULL;
    }
};

void Insertattail(node* &head,int value){
    node* n=new node(value);
    if(head==NULL){
        head=n;
        return;
    }

    node* temp=head;

    while(temp->next!=NULL){
        temp=temp->next;
    }
    temp->next=n;
}

void display(node* head){
    node* temp=head;

    while(temp!=NULL){
        cout<<temp->data<<"-> ";
        temp=temp->next;
    }
    cout<<endl;
}


int main(){

    node* head=NULL;
    int i;
    int m;
    cout<<"Enter the size of Array: "<<endl;
    cin>>m;
    int arr[m];
    int l=sizeof(arr)/sizeof(arr[0]);
      for(int i = 0 ;i < l ; i++)
        { 
            cout<<"Enter the elements of Array: "<<endl;
            cin>>arr[i];
        }



    Insertattail(head,arr[i]);
    display(head);


    return 0;

};
