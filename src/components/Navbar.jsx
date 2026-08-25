import React from 'react'
import { LineChart, Users, LogIn, User } from 'lucide-react'

export default function Navbar({ user, onOpenLogin, onOpenCreateGroup, onOpenJoinGroup, onOpenProfile }) {
  return (
    <nav class="bg-slate-900/95 backdrop-blur-md border-b border-slate-800 px-6 py-3.5 sticky top-0 z-50 flex justify-between items-center shadow-md">
      <div class="flex items-center space-x-3">
        <div class="bg-gradient-to-tr from-indigo-500 to-sky-400 p-2 rounded-2xl shadow-sm">
          <LineChart className="w-5 h-5 text-white" />
        </div>
        <span class="font-black text-xl text-white font-jua tracking-tight">
          같이투자 <span class="text-xs text-sky-300 font-normal">React Three Fiber</span>
        </span>
      </div>

      <div class="flex items-center gap-2 font-jua">
        <button
          onClick={onOpenCreateGroup}
          class="bg-indigo-950/90 hover:bg-indigo-900 text-indigo-200 px-3 py-1.5 rounded-xl text-xs font-bold border border-indigo-700/60 flex items-center gap-1.5 transition"
        >
          <Users className="w-3.5 h-3.5 text-indigo-400" /> 모임 만들기
        </button>
        <button
          onClick={onOpenJoinGroup}
          class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-700 flex items-center gap-1.5 transition"
        >
          <LogIn className="w-3.5 h-3.5 text-sky-400" /> 코드 참여
        </button>
        <button
          onClick={user?.id ? onOpenProfile : onOpenLogin}
          class="bg-gradient-to-r from-indigo-500 to-sky-400 text-white font-black text-xs px-3.5 py-1.5 rounded-xl transition shadow-md flex items-center gap-1.5"
        >
          <User className="w-3.5 h-3.5" />
          <span>{user?.nickname || '1초 소셜로그인'}</span>
        </button>
      </div>
    </nav>
  )
}
