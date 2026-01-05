package com.morzevichka.backend_api.infrastructure.jpa.entity;

import com.morzevichka.backend_api.domain.value.RouteType;
import jakarta.persistence.*;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Table;
import lombok.*;
import org.hibernate.annotations.*;
import org.hibernate.dialect.PostgreSQLEnumJdbcType;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Entity
@Table(name = "routes")
public class RouteEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Formula("chat_id")
    private Long chatId;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    @Enumerated(value = EnumType.STRING)
    @Column(name = "route_type", nullable = false)
    @JdbcTypeCode(SqlTypes.VARCHAR)
    private RouteType routeType = RouteType.PEDESTRIAN;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "chat_id", nullable = false, unique = true)
    private ChatEntity chat;

    @OneToMany(mappedBy = "route", fetch = FetchType.LAZY, cascade = CascadeType.ALL, orphanRemoval = true)
    private List<RoutePointEntity> routePoints = new ArrayList<>();

    @PrePersist
    public void prePersist() {
        this.updatedAt = LocalDateTime.now();
    }
}
