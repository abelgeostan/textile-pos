export type User={id:number;name:string;email:string;role:'admin'|'billing_staff'};
export const getUser=()=>{const x=localStorage.getItem('user'); return x?JSON.parse(x) as User:null};
export const logout=()=>{localStorage.clear();location.href='/login'};
