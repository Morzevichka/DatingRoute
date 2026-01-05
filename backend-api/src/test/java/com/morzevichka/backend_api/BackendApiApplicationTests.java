package com.morzevichka.backend_api;

import com.morzevichka.backend_api.infrastructure.redis.repository.CacheRouteRepository;
import com.morzevichka.backend_api.infrastructure.redis.repository.CacheUserRepository;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

@SpringBootTest
class BackendApiApplicationTests {
	@MockitoBean
	private CacheUserRepository cacheUserRepository;

	@MockitoBean
	private CacheRouteRepository cacheRouteRepository;

	@Test
	void contextLoads() {
	}

}
