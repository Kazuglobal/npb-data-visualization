import { useEffect, useState } from 'react';
import {
  SimpleGrid,
  Box,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  useColorModeValue,
} from '@chakra-ui/react';

interface Statistics {
  total_players: number;
  teams: number;
  last_updated: string;
}

export function Statistics() {
  const [stats, setStats] = useState<Statistics | null>(null);
  const bgColor = useColorModeValue('white', 'gray.800');

  useEffect(() => {
    async function fetchStatistics() {
      try {
        const response = await fetch('http://localhost:8000/statistics');
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.error('Error fetching statistics:', error);
      }
    }

    fetchStatistics();
  }, []);

  if (!stats) return null;

  return (
    <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
      <Box p={6} bg={bgColor} borderRadius="lg" boxShadow="sm">
        <Stat>
          <StatLabel>総選手数</StatLabel>
          <StatNumber>{stats.total_players}</StatNumber>
          <StatHelpText>全チーム合計</StatHelpText>
        </Stat>
      </Box>
      <Box p={6} bg={bgColor} borderRadius="lg" boxShadow="sm">
        <Stat>
          <StatLabel>チーム数</StatLabel>
          <StatNumber>{stats.teams}</StatNumber>
          <StatHelpText>NPB所属</StatHelpText>
        </Stat>
      </Box>
      <Box p={6} bg={bgColor} borderRadius="lg" boxShadow="sm">
        <Stat>
          <StatLabel>最終更新</StatLabel>
          <StatNumber>
            {new Date(stats.last_updated).toLocaleDateString('ja-JP')}
          </StatNumber>
          <StatHelpText>
            {new Date(stats.last_updated).toLocaleTimeString('ja-JP')}
          </StatHelpText>
        </Stat>
      </Box>
    </SimpleGrid>
  );
}