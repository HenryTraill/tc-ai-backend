import React, { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { authApi } from "~/data/api";

type AuthContextType = {
  user: any;
  loading: boolean;
};

const AuthContext = createContext<AuthContextType>({ user: null, loading: true });

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const res = await authApi.checkUser();
        if (!res) throw new Error("Not authenticated");
        setUser(res);
      } catch (error) {
        setUser(null);
        navigate("/login");
      } finally {
        setLoading(false);
      }
    }

    checkAuth();
  }, []);

  return <AuthContext.Provider value={{ user, loading }}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);