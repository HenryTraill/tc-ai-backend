import { useState } from 'react';
import { LogoIcon } from '~/svgs/logoIcon';
import type { Route } from './+types/login';
import { authApi } from '~/data/api';
import { useNavigate } from 'react-router';

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Login - TutorCruncher AI" },
    { name: "description", content: "Track student progress and lessons with TutorCruncher AI" },
  ];
}

const LoginPage = () => {
  const [email, setEmail] = useState('testing@tutorcruncher.com');
  const [password, setPassword] = useState('');
  const [error, setError] = useState("")
  const navigate = useNavigate();

  const handleSubmit = async (e: Event) => {
    e.preventDefault();

    try {
      const { access_token } = await authApi.login(email, password);
      localStorage.setItem("token", access_token);
      navigate("/")
    } catch {
      setError("Error, login details are incorrect")
    }
  }

  const handleTutorCruncherLogin = () => {
    console.log('Hello world');
  };

  return (
    <div className="min-h-screen bg-light-blue flex items-center justify-center p-6 font-sans">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-3xl shadow-2xl p-8 border border-navy-blue-15">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-dark-blue mb-2">Welcome Back</h1>
            <p className="text-navy-blue-50 text-sm">Sign in to your account to continue</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-semibold text-navy-blue-75 mb-2">
                Email Address
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-navy-blue-15 bg-grey focus:outline-none focus:ring-2 focus:ring-sky-blue focus:border-transparent transition-all duration-200 text-dark-blue placeholder-navy-blue-50"
                placeholder="Enter your email"
                required
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-semibold text-navy-blue-75 mb-2">
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-navy-blue-15 bg-grey focus:outline-none focus:ring-2 focus:ring-sky-blue focus:border-transparent transition-all duration-200 text-dark-blue placeholder-navy-blue-50"
                placeholder="Enter your password"
                required
              />
            </div>

            {/* Forgot Password Link */}
            <div className="text-right">
              <a href="#" className="text-sm text-sky-blue hover:text-steel-blue transition-colors duration-200 font-medium">
                Forgot your password?
              </a>
            </div>

            {error && <div className='text-red-600 border border-black p-3 text-center rounded-sm'>{error}</div>}

            <button
              type="submit"
              className="w-full bg-steel-blue text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-[1.02] shadow-lg hover:shadow-xl"
            >
              Sign In
            </button>
          </form >

          <div className="my-8 flex items-center">
            <div className="flex-1 border-t border-navy-blue-15"></div>
            <span className="px-4 text-sm text-navy-blue-50 font-medium">or</span>
            <div className="flex-1 border-t border-navy-blue-15"></div>
          </div>

          <button
            onClick={handleTutorCruncherLogin}
            className="w-full bg-white border-2 border-navy-blue-15 text-navy-blue-75 font-semibold py-3 px-6 rounded-xl hover:bg-grey hover:border-navy-blue-50 transition-all duration-200 flex items-center justify-center gap-3 shadow-sm hover:shadow-md"
          >
            <span className='w-6 h-6'>
              <LogoIcon />
            </span>
            Continue with TutorCruncher
          </button>



          <div className="mt-8 text-center">
            <p className="text-sm text-navy-blue-50">
              Don't have an account? {' '}
              <a href="#" className="text-sky-blue hover:text-steel-blue transition-colors duration-200 font-semibold">
                Sign up
              </a>
            </p>
          </div>
        </div >

        <div className="text-center mt-8">
          <p className="text-xs text-navy-blue-50">
            By signing in, you agree to our{' '}
            <a href="#" className="text-sky-blue hover:text-steel-blue transition-colors duration-200">
              Terms of Service
            </a>{' '}
            and{' '}
            <a href="#" className="text-sky-blue hover:text-steel-blue transition-colors duration-200">
              Privacy Policy
            </a>
          </p>
        </div>
      </div >
    </div >
  )
}

export default LoginPage;