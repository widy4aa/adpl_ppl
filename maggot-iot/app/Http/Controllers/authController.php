<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;

class AuthController extends Controller {
    // Halaman Login
    public function showLoginForm() {
        return view('livewire.login');
    }

    // Proses Login
    public function login(Request $request) {
        $credentials = $request->validate([
            'username' => 'required',
            'password' => 'required',
        ]);

        if (Auth::attempt($credentials)) {
            return redirect('/monitoring');
        }

        return back()->withErrors(['username' => 'username atau password salah.']);
    }
    // Logout
    public function logout() {
        Auth::logout();
        return redirect('/login');
    }
}
