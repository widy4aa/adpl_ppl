<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('keadaans', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('id_kandang');
            $table->date('recorded_date');
            $table->float('suhu_udara_min');
            $table->float('suhu_udara_max');
            $table->float('suhu_udara_avg');
            $table->float('suhu_tanah_min');
            $table->float('suhu_tanah_max');
            $table->float('suhu_tanah_avg');
            $table->float('kelembapan_udara_min');
            $table->float('kelembapan_udara_max');
            $table->float('kelembapan_udara_avg');
            $table->float('kelembapan_tanah_min');
            $table->float('kelembapan_tanah_max');
            $table->float('kelembapan_tanah_avg');

            $table->foreign('id_kandang')->references('id')->on('kandangs')->onUpdate('cascade')->onDelete('cascade');

        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('keadaans');
    }
};
