package com.suir.suir;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.IOException;

@SpringBootApplication
public class SuirApplication {
	public static void main(String[] args) {
			SpringApplication.run(SuirApplication.class, args);
	}

	/*public static void main(String[] args) {
		Backend backend = new Backend();
		try{
			backend.post();
		} catch (IOException e) {
			throw new RuntimeException(e);
		}

	}*/
}
