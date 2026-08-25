import React, { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Float, Sparkles, MeshWobbleMaterial } from '@react-three/drei'

function FloatingCoin({ position, color, scale = 1 }) {
  const meshRef = useRef()
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.8
      meshRef.current.rotation.x += delta * 0.4
    }
  })

  return (
    <Float speed={2.5} rotationIntensity={1.2} floatIntensity={1.8} position={position}>
      <mesh ref={meshRef} scale={scale}>
        <cylinderGeometry args={[1.2, 1.2, 0.3, 32]} />
        <meshStandardMaterial color={color} roughness={0.3} metalness={0.8} />
      </mesh>
    </Float>
  )
}

function BouncyCoreGem() {
  const coreRef = useRef()
  useFrame((state, delta) => {
    if (coreRef.current) {
      coreRef.current.rotation.x += delta * 0.3
      coreRef.current.rotation.y += delta * 0.5
    }
  })

  return (
    <Float speed={1.8} rotationIntensity={0.8} floatIntensity={1.2} position={[0, 0, -2]}>
      <mesh ref={coreRef} scale={2.8}>
        <octahedronGeometry args={[1, 0]} />
        <MeshWobbleMaterial color="#4f46e5" factor={0.4} speed={1.2} wireframe transparent opacity={0.35} />
      </mesh>
    </Float>
  )
}

export default function R3FCanvas() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 opacity-40">
      <Canvas camera={{ position: [0, 0, 12], fov: 50 }}>
        <ambientLight intensity={1.2} />
        <directionalLight position={[10, 10, 5]} intensity={1.5} color="#ffffff" />
        <pointLight position={[-10, -10, -5]} intensity={0.8} color="#38bdf8" />

        {/* Bouncy R3F 3D Core & Floating Elements */}
        <BouncyCoreGem />
        <FloatingCoin position={[-5, 2.5, 0]} color="#fbbf24" scale={0.9} />
        <FloatingCoin position={[5, -2, 1]} color="#6366f1" scale={1.1} />
        <FloatingCoin position={[-3, -3, -1]} color="#38bdf8" scale={0.7} />
        <FloatingCoin position={[4, 3, -2]} color="#a855f7" scale={0.85} />

        {/* Ambient R3F Sparkles */}
        <Sparkles count={60} scale={18} size={2.5} speed={0.4} color="#6366f1" />
      </Canvas>
    </div>
  )
}
