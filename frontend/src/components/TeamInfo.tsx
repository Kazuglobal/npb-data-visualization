import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Heading,
  Text,
  Image,
  VStack,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Spinner,
  Alert,
  AlertIcon,
  useColorModeValue,
} from '@chakra-ui/react';

interface TeamData {
  name: {
    ja: string;
    en: string;
  };
  details: {
    [key: string]: string;
  };
  logo_url?: string;
}

interface TeamInfoProps {
  league?: 'central' | 'pacific';
}

export default function TeamInfo({ league }: TeamInfoProps) {
  const [teams, setTeams] = useState<{ central: TeamData[]; pacific: TeamData[] }>({
    central: [],
    pacific: [],
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  useEffect(() => {
    fetchTeams();
    fetchLastUpdated();
  }, []);

  const fetchTeams = async () => {
    try {
      const response = await fetch('http://localhost:8000/teams');
      if (!response.ok) {
        throw new Error('Failed to fetch team data');
      }
      const data = await response.json();
      setTeams(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchLastUpdated = async () => {
    try {
      const response = await fetch('http://localhost:8000/teams/last_updated');
      if (response.ok) {
        const data = await response.json();
        setLastUpdated(new Date(data.last_updated).toLocaleString());
      }
    } catch (err) {
      console.error('Failed to fetch last updated timestamp:', err);
    }
  };

  const renderTeamCard = (team: TeamData) => (
    <Box
      p={6}
      borderWidth="1px"
      borderRadius="lg"
      bg={bgColor}
      borderColor={borderColor}
      shadow="md"
    >
      <VStack spacing={4} align="stretch">
        <Box textAlign="center">
          {team.logo_url && (
            <Image
              src={team.logo_url}
              alt={`${team.name.ja} logo`}
              maxH="100px"
              mx="auto"
              mb={4}
            />
          )}
          <Heading size="md" mb={2}>
            {team.name.ja}
          </Heading>
          <Text color="gray.500" fontSize="sm">
            {team.name.en}
          </Text>
        </Box>

        <Grid templateColumns="auto 1fr" gap={4}>
          {Object.entries(team.details).map(([key, value]) => (
            <React.Fragment key={key}>
              <Text fontWeight="bold">{key}:</Text>
              <Text>{value}</Text>
            </React.Fragment>
          ))}
        </Grid>
      </VStack>
    </Box>
  );

  if (isLoading) {
    return (
      <Box textAlign="center" py={8}>
        <Spinner />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert status="error">
        <AlertIcon />
        {error}
      </Alert>
    );
  }

  if (league) {
    return (
      <Box>
        {lastUpdated && (
          <Text fontSize="sm" color="gray.500" mb={4}>
            最終更新: {lastUpdated}
          </Text>
        )}
        <Grid
          templateColumns="repeat(auto-fit, minmax(300px, 1fr))"
          gap={6}
          p={4}
        >
          {teams[league].map((team, index) => (
            <Box key={index}>{renderTeamCard(team)}</Box>
          ))}
        </Grid>
      </Box>
    );
  }

  return (
    <Box>
      {lastUpdated && (
        <Text fontSize="sm" color="gray.500" mb={4}>
          最終更新: {lastUpdated}
        </Text>
      )}
      <Tabs>
        <TabList>
          <Tab>セ・リーグ</Tab>
          <Tab>パ・リーグ</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <Grid
              templateColumns="repeat(auto-fit, minmax(300px, 1fr))"
              gap={6}
            >
              {teams.central.map((team, index) => (
                <Box key={index}>{renderTeamCard(team)}</Box>
              ))}
            </Grid>
          </TabPanel>
          <TabPanel>
            <Grid
              templateColumns="repeat(auto-fit, minmax(300px, 1fr))"
              gap={6}
            >
              {teams.pacific.map((team, index) => (
                <Box key={index}>{renderTeamCard(team)}</Box>
              ))}
            </Grid>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
}