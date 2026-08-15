"use client";
import {createContext,useContext,useEffect,useState} from "react";
export type CurrentUser={id:number;username:string;email:string};
const UserContext=createContext<{user:CurrentUser|null;refresh:()=>void}>({user:null,refresh:()=>{}});
export function UserProvider({children}:{children:React.ReactNode}){const [user,setUser]=useState<CurrentUser|null>(null);const refresh=()=>{const adminUser=localStorage.getItem('admin_user');if(adminUser){try{setUser(JSON.parse(adminUser));return}catch{}}const token=localStorage.getItem('token');if(!token){setUser(null);return}fetch('http://127.0.0.1:8000/me',{headers:{Authorization:`Bearer ${token}`}}).then(r=>r.ok?r.json():null).then(setUser).catch(()=>setUser(null))};useEffect(refresh,[]);return <UserContext.Provider value={{user,refresh}}>{children}</UserContext.Provider>}
export const useUser=()=>useContext(UserContext);
