<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Carbon\Carbon;

class MaggotSeeder extends Seeder
{
    public function run(): void
    {
        $userId = DB::table('users')->insertGetId([
            'username' => 'widy4aa',
            'password' => Hash::make('dio'),
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        $kandangId = DB::table('kandangs')->insertGetId([
            'id_user' => $userId,
            'name' => 'Kandang Maggot 1',
            'location' => 'Jember',
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        $deviceId = DB::table('device_ids')->insertGetId([
            'id_kandang' => $kandangId,
            'device_name' => 'esp32_001'
        ]);

        $controlId = DB::table('device_controls')->insertGetId([
            'id_device' => $deviceId,
            'mode' => 'otomatis',
            'status' => 'off',
        ]);

        $configId = DB::table('device_configurations')->insertGetId([
            'id_device_control' => $controlId,
            'suhu_min' => 27.0,
            'suhu_max' => 35.0,
            'kelembapan_min' => 50.0,
            'kelembapan_max' => 80.0,
            'kelembapan_tanah_min' => 30.0,
            'kelembapan_tanah_max' => 70.0,
            'mode_auto' => true,
            'updated_at' => now(),
        ]);

        DB::table('device_schedules')->insert([
            'id_device_configurations' => $configId,
            'scheduled_time' => '08:00:00',
            'duration_minutes' => 10,
            'repeat_daily' => true,
        ]);

        DB::table('keadaans')->insert([
            'id_kandang' => $kandangId,
            'recorded_date' => Carbon::now()->toDateString(),
            'suhu_udara_min' => 28.0,
            'suhu_udara_max' => 30.0,
            'suhu_udara_avg' => 29.0,
            'suhu_tanah_min' => 26.0,
            'suhu_tanah_max' => 28.0,
            'suhu_tanah_avg' => 27.0,
            'kelembapan_udara_min' => 65.0,
            'kelembapan_udara_max' => 75.0,
            'kelembapan_udara_avg' => 70.0,
            'kelembapan_tanah_min' => 50.0,
            'kelembapan_tanah_max' => 60.0,
            'kelembapan_tanah_avg' => 55.0,
        ]);

        DB::table('statuses')->insert([
            'id_kandang' => $kandangId,
            'status_kandang' => 'baik',
            'penyebab' => 'Normal semua',
            'created_at' => now(),
            'updated_at' => now(),
        ]);
    }
}
