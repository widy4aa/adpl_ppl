<?php

use App\Http\Controllers\authController;
use App\Livewire\Monitoring;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});


Route::get('/monitoring', Monitoring::class)->name('monitoring')->middleware('auth')->name('monitoring');

Route::get('/login', [authController::class, 'showLoginForm'])->name('login');
Route::post('/login', [authController::class, 'login']);
Route::post('/logout',[authController::class,'logout']);
Route::get('/register', [AuthController::class, 'showRegister'])->name('register');
Route::post('/register', [AuthController::class, 'register']);
